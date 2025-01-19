import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Large CSV Viewer",
    layout="wide"
)

# Title and Description
st.title("Large CSV Viewer 📂")
st.markdown("""
Upload your CSV file (up to 70 MB), and this app will let you view and explore the data interactively.
""")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load CSV into a pandas DataFrame
        with st.spinner("Loading your data..."):
            # Specify chunk size to handle large files efficiently
            chunk_size = 100000  # Number of rows per chunk
            data_chunks = pd.read_csv(uploaded_file, chunksize=chunk_size)
            
            # Concatenate chunks
            df = pd.concat(data_chunks, ignore_index=True)

        st.success(f"File loaded successfully! {len(df)} rows and {len(df.columns)} columns.")
        
        # Display the first few rows
        st.subheader("Preview of the Data")
        st.dataframe(df.head(100))  # Display first 100 rows
        
        # Provide data summary
        st.subheader("Data Overview")
        st.write("Shape of the data:")
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.write("Column names:")
        st.write(list(df.columns))
        
        # Option to filter columns
        st.subheader("Explore Data")
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=df.columns,
            default=df.columns[:5]  # Default to the first 5 columns
        )
        
        if selected_columns:
            st.dataframe(df[selected_columns].head(100))
        
        # Download option
        st.subheader("Download Processed File")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_file.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
