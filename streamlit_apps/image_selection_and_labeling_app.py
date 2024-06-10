import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Set page configuration to wide mode
st.set_page_config(layout="wide")

figure_pages_viewed_path = 'fig_pages_viewed_example.xlsx'
cropped_and_labeled_figures_path = 'cropped_and_labeled_figs_example.xlsx'
final_figures_path = 'final_figures_folder_example'

# Load the data from the Excel file
@st.cache_data
def load_data():
    path = 'extracted_figure_pages_example.xlsx'
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


def add_image_data(current_data, new_image_path):
    labeled_data = load_labeled_data()
    
    # Check if a row with the same figure name exists
    if not labeled_data[labeled_data['figure name'] == current_data['figure name']].empty:
        st.info('Image already labeled and saved.')
        return
    
    # Add new row with data from the original df and additional info
    new_row = current_data.copy()
    new_row['new image path'] = new_image_path
    new_row['subcategory'] = ''  # Initially empty, to be filled later

    # Append new row to the DataFrame
    labeled_data = labeled_data.append(new_row, ignore_index=True)
    save_labeled_data(labeled_data)
    st.success(f"New image data saved: {new_image_path}")


# Create three columns with specified width ratios
left_column, middle_column, right_column = st.columns([3, 4.5, 4.5])

subcategories = [
    "Process Diagram",
    "2x2 Matrix",
    "Venn Diagram",
    "Conceptual Diagram",
    "Cycle",
    "Hierarchical Diagram",
    "Bar Chart",
    "Stacked Bar Chart",
    "Line Graph",
    "Data structure",
    "Data display",
    "Data maps",
    "Data collection, data analysis, data gathering diagrams",
    "Heatmap",
    "Data Map",
    "Organizational Chart",
    "Timeline",
    "Drawing",
    "Photo"
]

with left_column:  # Use the left column for selections and displaying the DataFrame
    st.header("1. Figure Page Select")
    year = st.selectbox('Select a Year:', range(2020, 2023), index=0)
    filtered_df = df[df['year'] == year]
    if not filtered_df.empty:
        if 'current_image_index' not in st.session_state:
            st.session_state.current_image_index = 0
        
        current_idx = 0
        if(st.session_state.current_image_index):
            current_idx = st.session_state.current_image_index 
        max_idx = len(filtered_df) - 1

        if st.button('Previous', key='prev_button', use_container_width=True):
            if current_idx > 0:
                st.session_state.current_image_index -= 1

        if st.button('Next', key='next_button', use_container_width=True):
            if current_idx < max_idx:
                st.session_state.current_image_index += 1

        highlight = filtered_df.index[current_idx]
        st.dataframe(filtered_df.style.apply(lambda x: ['background-color: yellow' if x.name == highlight else '' for i in x], axis=1), height=700)
    else:
        st.write("No data available for this year.")


with middle_column:
    st.header("2. Crop Figure")
    if not filtered_df.empty:
        current_data = filtered_df.iloc[current_idx]
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

        image_path = os.path.join('extracted_figure_pages_example', str(year), figure_name)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            canvas_width = 700
            aspect_ratio = image.width / image.height
            canvas_height = int(canvas_width / aspect_ratio)

            # Setup canvas drawing mode dynamically
            if 'rect_drawn' not in st.session_state:
                st.session_state.rect_drawn = False
            drawing_mode = "rect" if not st.session_state.rect_drawn else "transform"

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)", 
                stroke_width=2,
                stroke_color="#ffffff",
                background_image=image,
                update_streamlit=True,
                width=canvas_width,
                height=canvas_height,
                drawing_mode=drawing_mode,
                key="canvas",
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
                    save_path = os.path.join(image_directory, figure_name + '.png')
                    crop.save(save_path)
                    st.success(f"Saved cropped image to {save_path}")

        else:
            st.error("Image file not found.")
    else:
        st.write("No image to display.")


with right_column:
    st.header("3. Categorize Figure")
    # Example usage inside your existing code
    if 'crop' in st.session_state:
        # Save the cropped image
        save_path = os.path.join(image_directory, figure_name + '.png')
        crop.save(save_path)
        st.success(f"Saved cropped image to {save_path}")

        # Add data for the saved image
        add_image_data(current_data, save_path)
    else:
        # Check if there is an existing image and no new canvas drawn
        labeled_data = load_labeled_data()
        existing_image = labeled_data[labeled_data['figure name'] == current_data['figure name']]['new image path'].values
        if existing_image:
            st.image(existing_image[0], caption="Previously saved image")
        else:
            st.write("No image to display.")