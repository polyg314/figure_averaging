import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Set page configuration to wide mode
st.set_page_config(layout="wide")

figure_pages_viewed_path = 'fig_pages_viewed.xlsx'
cropped_and_labeled_figures_path = 'cropped_and_labeled_figs.xlsx'
final_figures_path = 'final_figures'

# Load the data from the Excel file
# @st.cache_data
def load_data():
    path = 'extracted_figure_pages.xlsx'
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        return pd.DataFrame()

df = load_data()


def load_viewed_data():
    # Check if data is already loaded in the session state
    if 'viewed_data' not in st.session_state or st.session_state.viewed_data is None:
        if os.path.exists(figure_pages_viewed_path):
            # Load data from Excel and store it in session state
            st.session_state.viewed_data = pd.read_excel(figure_pages_viewed_path)
        else:
            # Initialize an empty DataFrame in session state if the file does not exist
            st.session_state.viewed_data = pd.DataFrame()
    return st.session_state.viewed_data

# Save the updated DataFrame to the Excel file
def save_viewed_data(df):
    # Save the DataFrame to the Excel file
    df.to_excel(figure_pages_viewed_path, index=False)
    # Update the session state with the new data
    st.session_state.viewed_data = df

viewed_df = load_viewed_data()

def load_labeled_data():
    if 'labeled_data' not in st.session_state or st.session_state.labeled_data is None:
        if os.path.exists(cropped_and_labeled_figures_path):
            st.session_state.labeled_data = pd.read_excel(cropped_and_labeled_figures_path)
        else:
            st.session_state.labeled_data = pd.DataFrame()
    return st.session_state.labeled_data

def save_labeled_data(df):
    df.to_excel(cropped_and_labeled_figures_path, index=False)
    st.session_state.labeled_data = df


def add_image_data(current_data, new_image_path, subcategory=''):
    labeled_data = load_labeled_data()
    
    # Check if a row with the same figure name exists
    if not labeled_data[labeled_data['figure name'] == current_data['figure name']].empty:
        st.info('Image already labeled and saved.')
        return
    
    # Add new row with data from the original df and additional info
    new_row = current_data.copy()
    new_row['new image path'] = new_image_path
    new_row['subcategory'] = subcategory  # Set the subcategory

    # Create a DataFrame from new_row and append it to labeled_data using pd.concat
    new_row_df = pd.DataFrame([new_row])
    labeled_data = pd.concat([labeled_data, new_row_df], ignore_index=True)

    save_labeled_data(labeled_data)
    st.success(f"New image data saved: {new_image_path}")

# Create three columns with specified width ratios
left_column, middle_column, right_column = st.columns([3, 5, 4])

subcategories = [
    "None Selected",
    "Process Diagram",
    "2x2 Matrix",
    "Venn Diagram",
    "Conceptual Diagram",
    "Cycle",
    "Hierarchical Diagram",
    "Bar Chart",
    "Stacked Bar Chart",
    "Line Graph",
    "Scatter Plot",
    "Mixed statistical plot (more than 1 statistical plot type)",
    "Data structure",
    "Data collection, data analysis, data gathering diagrams",
    "Heatmap",
    "Data Map",
    "Organizational Chart",
    "Timeline",
    "Drawing",
    "Photo"
]


# In the following, I am going to provide figures from different peer-reviewed papers, and I want you to classify them according to the following categories each time an new image is passed: 

# Categories: "process diagram", "2x2 matrix", "venn diagram", "conceptual diagram", "cycle", "hierarchical diagram", "bar chart", "stacked bar chart", "line graph", "scatter plot", "mixed statistical plot (more than 1 statistical plot type)", "data structure", "data collection, data analysis, data gathering diagrams", "heatmap", "data map", "organizational chart", "timeline", "drawing", "photo"

# Please choose the category that best represents and most specifically describes the image. Your response should only be an exact string matching one of the categories. 

# If you are ready for me to send images, respond with “OK, ready”.



def compute_view_status(filtered_df, viewed_df, key_columns):
    # Initialize 'is_viewed' to False for all rows in filtered_df
    filtered_df['is_viewed'] = False
    
    # Create a DataFrame with just the key columns and a dummy column to mark as viewed
    viewed_keys = viewed_df[key_columns].drop_duplicates()
    viewed_keys['is_viewed'] = True  # Explicitly mark these as viewed
    
    # Perform the merge; this will only affect rows where there's a match
    merge_result = pd.merge(filtered_df, viewed_keys, on=key_columns, how='left', suffixes=('', '_from_viewed'))
    
    # After the merge, update 'is_viewed' where there are matches and only if 'is_viewed_from_viewed' is True
    merge_result['is_viewed'] = np.where(
        merge_result['is_viewed_from_viewed'] == True,  # Condition
        merge_result['is_viewed_from_viewed'],          # Value if condition is True
        merge_result['is_viewed']                       # Value if condition is False
    ).astype(bool)

    # Clean up by dropping the temporary column used for merging
    merge_result.drop(columns='is_viewed_from_viewed', inplace=True)
    
    return merge_result



iniital_index = 0


with left_column:  # Use the left column for selections and displaying the DataFrame
    st.header("1. Figure Page Select")
    year = st.selectbox('Select a Year:', range(2022, 1999, -1), index=list(range(2022, 1999, -1)).index(2022))

    if year != st.session_state.get('year', None):
        st.session_state.year = year
        st.session_state.current_image_index = iniital_index  # Reset index when year changes

    # Filter data based on selected year
    filtered_df = df[df['year'] == year]
    filtered_df = filtered_df.sort_values(by=['original paper', 'figure number', 'page number']).reset_index(drop=True)

    # Define columns to check for match
    key_columns = ['original paper', 'figure name', 'figure number', 'year', 'page number']

    if not filtered_df.empty:
        if 'current_image_index' not in st.session_state:
            st.session_state.current_image_index = iniital_index
        
        current_idx = iniital_index
        if st.session_state.current_image_index:
            current_idx = st.session_state.current_image_index 
        max_idx = len(filtered_df) - 1

        def style_rows(row):
            if(row.name == current_idx):
                color = 'background-color: yellow'
            else: 
                # Determine the background color based on the 'is_viewed' status
                color = 'background-color: lightgreen' if row['is_viewed'] else 'background-color: #FF8B72'
            return [color] * len(row)

        if st.button('Previous', key='prev_button', use_container_width=True):
            if current_idx > 0:
                st.session_state.current_image_index -= 1
                st.session_state.rect_drawn = False
                if 'crop' in st.session_state:
                    del st.session_state['crop']

        if st.button('Next', key='next_button', use_container_width=True):
            if current_idx < max_idx:
                st.session_state.current_image_index += 1
                st.session_state.rect_drawn = False
                if 'crop' in st.session_state:
                    del st.session_state['crop']

        highlight = filtered_df.index[current_idx]
        filtered_df = compute_view_status(filtered_df, viewed_df, key_columns)
        styled_df = filtered_df.style.apply(style_rows, axis=1)
        
        st.dataframe(styled_df, height=700)
        st.write(f"Files still need to go through: {len(filtered_df[filtered_df['is_viewed'] == False])}")
    else:
        st.write("No data available for this year.")


with middle_column:
    st.header("2. Crop Figure")
    if not filtered_df.empty:
        current_data = filtered_df.iloc[st.session_state.current_image_index]
        columns_to_check = ['original paper', 'figure name', 'figure number', 'year', 'page number']

        # Check if the current data row is already in the viewed data based on specified columns
        if not ((viewed_df[columns_to_check] == current_data[columns_to_check]).all(axis=1)).any():
            viewed_df = pd.concat([viewed_df, current_data.to_frame().T], ignore_index=True)
            save_viewed_data(viewed_df)

        year = current_data['year']  # Get year from current data
        figure_name = current_data['figure name']  # Get figure name from current data
        image_directory = os.path.join(final_figures_path, str(year))

        # Ensure the directory exists
        os.makedirs(image_directory, exist_ok=True)

        image_path = os.path.join('extracted_figure_pages', str(year), figure_name)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            canvas_width = 700
            aspect_ratio = image.width / image.height
            canvas_height = int(canvas_width / aspect_ratio)

            # Ensure session state is initialized properly
            if 'rect_drawn' not in st.session_state:
                st.session_state.rect_drawn = False

            if 'current_image_index' not in st.session_state:
                st.session_state.current_image_index = 0  # Initialize if not already set


            # Setup canvas drawing mode dynamically
            if 'rect_drawn' not in st.session_state:
                st.session_state.rect_drawn = False
            drawing_mode = "rect" if not st.session_state.rect_drawn else "transform"

            canvas_key = f"canvas_{image_path}"

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#ffffff",
                background_image=image,
                update_streamlit=True,
                width=canvas_width,
                height=canvas_height,
                drawing_mode=drawing_mode,
                key=canvas_key,
            )

            if canvas_result.json_data is not None and 'objects' in canvas_result.json_data:
                st.session_state.rect_drawn = True
                objects = pd.json_normalize(canvas_result.json_data["objects"])
                if not objects.empty:
                    # Calculate the absolute position and size in the original image
                    coords = objects.iloc[0][["left", "top", "width", "height", "scaleX", "scaleY"]]
                    x0 = int(coords["left"] * image.width / canvas_width)
                    y0 = int(coords["top"] * image.height / canvas_height)
                    x1 = int((coords["left"] + coords["width"] * coords["scaleX"]) * image.width / canvas_width)
                    y1 = int((coords["top"] + coords["height"] * coords["scaleY"]) * image.height / canvas_height)

                    # Crop the image based on calculated coordinates
                    crop = image.crop((x0, y0, x1, y1))
                    st.session_state["crop"] = crop

                    # Save the cropped image
                    save_path = os.path.join(image_directory, figure_name)
                    crop.save(save_path)
                    st.success(f"Saved cropped image to {save_path}")
                     # Add data for the saved image
                    add_image_data(current_data, save_path)
        else:
            st.error("Image file not found.")
    else:
        st.write("No image to display.")






with right_column:
    st.header("3. Categorize Figure")

    labeled_data = load_labeled_data()

    # Attempt to fetch current figure data and existing image
    existing_entry = labeled_data[labeled_data['figure name'] == current_data['figure name']]
    current_subcategory = existing_entry['subcategory'].iloc[0] if not existing_entry.empty else None

    if not existing_entry.empty:
        # Setup radio buttons for subcategories
        radio_key = f"radio_{st.session_state.current_image_index}{str(year)}"
        selected_subcategory = st.radio(
            "Select Subcategory:",
            subcategories,
            index=subcategories.index(current_subcategory) if current_subcategory in subcategories else 0,
            key=radio_key
        )

    # If a cropped image exists in the session state, save it and update the subcategory
    if 'crop' in st.session_state:
        save_path = os.path.join(image_directory, figure_name)
        crop.save(save_path)
        st.image(save_path, caption="Cropped Image")
        # st.success(f"Saved cropped image to {save_path}")

        # Update or add image data with subcategory
        if not existing_entry.empty:
            # Update existing entry
            labeled_data.loc[labeled_data['figure name'] == current_data['figure name'], 'subcategory'] = selected_subcategory
            save_labeled_data(labeled_data)
            if not existing_entry.empty and existing_entry['subcategory'].iloc[0] != selected_subcategory:
                if(selected_subcategory != "None Selected"):
                    st.success("Subcategory updated")
        else:
            # Add new data entry
            add_image_data(current_data, save_path, selected_subcategory)

        # Display the cropped image

    else:
        # Handle the case when no crop is present but existing data might be shown
        if existing_entry.empty:
            st.write("No image to categorize or display.")
        else:
            # Display existing labeled image if present
            existing_image_path = existing_entry['new image path'].iloc[0]
            st.image(existing_image_path, caption="Previously saved image")

            # Update the subcategory if it has changed
            if selected_subcategory != current_subcategory:
                labeled_data.loc[labeled_data['figure name'] == current_data['figure name'], 'subcategory'] = selected_subcategory
                save_labeled_data(labeled_data)
                st.success("Subcategory updated")
