import os
import zipfile
import streamlit as st
from utils import *
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def extract_zip(file_path, extract_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_info.filename = os.path.basename(file_info.filename)
            zip_ref.extract(file_info, extract_path)
    # Check if the zip file exists
    # with zipfile.ZipFile("temp.zip", "r") as zip_ref:
    #         zip_ref.extractall("data")
        
    # # Get all audio files in the directory
    # audio_files_directory = "data"
    # audio_files = [os.path.join(audio_files_directory, f) for f in os.listdir(audio_files_directory) if f.endswith(".mp3")]


with st.sidebar:

    st.title("File Uploader")

    uploaded_file = st.file_uploader("Upload a folder or a zip file", type=["zip", "folder"], accept_multiple_files=False)

    if uploaded_file is not None:

        file_name = uploaded_file.name
        file_ext = file_name.split('.')[-1]

        if file_ext == "zip":
            extract_path = "files"
            os.makedirs(extract_path, exist_ok=True)
            extract_zip(file_name, extract_path)
            st.success(f"Files extracted from {file_name} and saved to {extract_path}.")
        else:
            folder_path = "files"
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"{file_name} saved to {folder_path}.")

        if any(os.listdir("files")):
            result = process()
if uploaded_file is not None:
    if not any(os.listdir("files")):
        st.warning("Upload files to view the insights")
    else:
        st.header("Silent Ratio")
        for filename in os.listdir('files'):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                # Construct the full path to the audio file
                audio_file_path = os.path.join('files', filename)
                
                # Calculate silence ratio for the current audio file
                silence_ratio = calculate_silence_ratio(audio_file_path)
                
                # Display filename along with silence ratio using Streamlit
                st.write(f"{filename[:-4]}: {silence_ratio}")

        st.header("OverRall call Ratio")
        st.write(ovr_r())

        st.header("Insights")
        df2= pd.read_csv("data.csv", header=None, names=["Caller_id", "Insights"])
        # print(df2)
        for index, row in df2.iterrows():
            # Display the caller_id
            st.write(f"{' ' * 30} {row['Caller_id']}")
            # Display the insights
            st.write(f"{' ' * 30} {row['Insights']}")


        # Convert data to DataFrame
        df = pd.read_csv('vis.csv')

        # Streamlit app
        st.title('Charts for Call Data')

        # Generate separate charts for each variable
        for column in df.columns:
            if column != 'Call_id':
                # st.header(f'Charts for {column}')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                
                # Create a figure with two subplots
                fig, axes = plt.subplots(1, 2, figsize=(10, 5))

                # Bar chart on the left
                sns.countplot(data=df, x=column, ax=axes[0])
                axes[0].set_title(f'Count of {column}')

                # Pie chart on the right
                df[column].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[1])
                axes[1].set_title(f'Distribution of {column}')

                # Show the plots
                st.pyplot(fig)

    
