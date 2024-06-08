import streamlit as st
import pandas as pd
import os

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

with left_column:  # Use the left column for selections and displaying the DataFrame
    # Select a year using a dropdown
    year = st.selectbox('Select a Year:', range(1965, 2025), index=0)  # Default to the first year

    # Display DataFrame filtered by the selected year
    filtered_df = df[df['year'] == year]
    if not filtered_df.empty:
        # Navigation buttons and current selection display
        if 'current_image_index' not in st.session_state:
            st.session_state.current_image_index = 0

        max_idx = len(filtered_df) - 1
        current_idx = st.session_state.current_image_index

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Previous'):
                if current_idx > 0:
                    st.session_state.current_image_index -= 1
        with col2:
            if st.button('Next'):
                if current_idx < max_idx:
                    st.session_state.current_image_index += 1

        # Display the currently selected row highlighted in the dataframe
        st.write("Current Selection in DataFrame:")
        highlight = filtered_df.index[current_idx]
        st.dataframe(filtered_df.style.apply(lambda x: ['background-color: yellow' if x.name == highlight else '' for i in x], axis=1))
    else:
        st.write("No data available for this year.")

with middle_column:  # Use the middle column for image display
    if not filtered_df.empty:
        # Display current image
        image_path = os.path.join('extracted_figure_pages', str(year), filtered_df.iloc[current_idx]['figure name'])
        if os.path.exists(image_path):
            st.image(image_path, caption=filtered_df.iloc[current_idx]['figure name'])
        else:
            st.error("Image file not found.")
    else:
        st.write("No image to display.")

# The right column is intentionally left empty for now
with right_column:
    st.write("Additional content can be added here.")



# Figure classification 

# “Group Comparison”, “Cycles”, “Process”, “Timeline”, “Group Comparison Timeline” 

# Figure type 

# “Histograms or Bar Chart”, “Diagram”, “Line Graph”, “Heatmap”, “Chart”, 

