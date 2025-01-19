import streamlit as st
import pandas as pd

# Set page configuration to full screen
st.set_page_config(
    page_title="Robust CSV Viewer",
    layout="wide"  # Allows content to stretch across the screen
)

# Title and Description
st.title("Full-Page Robust CSV Viewer 📂")
st.markdown("""
This app loads and displays your CSV file, maximizing the viewport for easier data navigation.
Problematic rows are automatically skipped.
""")

# Google Drive File URL
drive_file_url = "https://drive.google.com/file/d/1FM4f9e__SW5F5sHrY5Z_Dk0r70mADiDb/view?usp=sharing"

try:
    # Convert Google Drive link to direct download link
    file_id = drive_file_url.split('/d/')[1].split('/view')[0]
    direct_url = f"https://drive.google.com/uc?id={file_id}"
    
    # Load the CSV file in chunks
    chunk_size = 100000
    data_chunks = []

    with st.spinner("Loading data in chunks..."):
        for chunk in pd.read_csv(direct_url, chunksize=chunk_size, on_bad_lines='skip'):
            data_chunks.append(chunk)

    # Combine all valid chunks into a single DataFrame
    df = pd.concat(data_chunks, ignore_index=True)
    st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns after skipping errors.")

    # Data Preview with full-page viewport
    st.subheader("Full-Page Data Preview")
    st.markdown(
        """
        Use the table below to interact with the data. Scroll horizontally and vertically to explore all rows and columns.
        """
    )
    st.dataframe(df, use_container_width=True, height=800)  # Fill page width, large height

    # Data Overview
    st.subheader("Data Overview")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write("Column Names:", list(df.columns))

    # Column Selection for Exploration
    st.subheader("Explore Data")
    selected_columns = st.multiselect(
        "Select columns to display:",
        options=df.columns,
        default=df.columns[:min(len(df.columns), 5)]  # Default to the first 5 columns
    )
    if selected_columns:
        st.dataframe(df[selected_columns], use_container_width=True, height=600)

    # Allow Download of Valid Data
    st.subheader("Download Cleaned Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Failed to load data: {e}")
