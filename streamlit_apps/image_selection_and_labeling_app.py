import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Load the data from the Excel file
@st.cache_data
def load_data():
    path = 'extracted_figure_pages_example.xlsx'
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        return pd.DataFrame()

df = load_data()

# Create three columns with specified width ratios
left_column, middle_column, right_column = st.columns([3, 4.5, 4.5])

categories = {
    "Statistical Graphs": [
        "Bar Chart",
        "Stacked Bar Chart",
        "Line Graph"
    ],
    "Informational Diagrams": [
        "Process Diagram",
        "2x2 Matrix",
        "Venn Diagram",
        "Conceptual Diagram",
        "Timeline",
        "Cycle",
        "Hierarchical Diagram",
        "Organizational Chart"
    ],
    "Spatial and Data-Intensive Visualizations": [
        "Heatmap",
        "Data Map"
    ],
    "Visual Media": [
        "Drawing",
        "Photo"
    ]
}

subcategories = [
    "Bar Chart", "Stacked Bar Chart", "Line Graph", "Process Diagram", "2x2 Matrix", 
    "Venn Diagram", "Conceptual Diagram", "Timeline", "Cycle", "Hierarchical Diagram", 
    "Organizational Chart", "Heatmap", "Data Map", "Drawing", "Photo"
]


with left_column:  # Use the left column for selections and displaying the DataFrame
    st.header("1. Page Image Select")
    year = st.selectbox('Select a Year:', range(1965, 2025), index=0)
    filtered_df = df[df['year'] == year]
    if not filtered_df.empty:
        if 'current_image_index' not in st.session_state:
            st.session_state.current_image_index = 0
        current_idx = st.session_state.current_image_index
        max_idx = len(filtered_df) - 1

        if st.button('Previous'):
            if current_idx > 0:
                st.session_state.current_image_index -= 1
        if st.button('Next'):
            if current_idx < max_idx:
                st.session_state.current_image_index += 1

        highlight = filtered_df.index[current_idx]
        st.dataframe(filtered_df.style.apply(lambda x: ['background-color: yellow' if x.name == highlight else '' for i in x], axis=1))
    else:
        st.write("No data available for this year.")

with middle_column:
    st.header("2. Crop Figure")
    if not filtered_df.empty:
        image_path = os.path.join('extracted_figure_pages', str(year), filtered_df.iloc[current_idx]['figure name'])
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
                    # Access the first object which is the drawn or transformed rectangle
                    coords = objects.iloc[0][["left", "top", "width", "height", "scaleX", "scaleY"]]
                    coords["width"] = coords["width"]*coords["scaleX"]
                    coords["height"] = coords["height"]*coords["scaleY"]
                    scale_x = image.width / canvas_width  # Scale factor for width
                    scale_y = image.height / canvas_height  # Scale factor for height

                    # Correctly apply scaling to calculate the absolute position and size in the original image
                    x0 = coords["left"] * scale_x
                    y0 = coords["top"] * scale_y
                    x1 = (coords["left"] + coords["width"]) * scale_x
                    y1 = (coords["top"] + coords["height"]) * scale_y

                    # Crop the image based on calculated coordinates
                    crop = image.crop((x0, y0, x1, y1))
                    st.session_state["crop"] = crop
        else:
            st.error("Image file not found.")
    else:
        st.write("No image to display.")

with right_column:
    st.header("3. Categorize Figure")
    if "crop" in st.session_state:
        st.image(st.session_state["crop"], caption="Cropped Image")
        # Display subcategories as vertical radio buttons
        subcategory = st.radio("", subcategories, key='subcategory')
    else:
        st.write("Draw a rectangle on the image to see the cropped area here.")