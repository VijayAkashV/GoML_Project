import zipfile
import os
from pydub import AudioSegment
from pydub import AudioSegment
import requests
from lyzr import VoiceBot
import csv
import pandas as pd
import altair as alt
import streamlit as st
import librosa

def calculate_silence_ratio(audio_file_path, min_long_silence_duration=2.0):
    # Load audio file
    audio_data, _ = librosa.load(audio_file_path, sr=None)

    # Calculate silent intervals using librosa.effects.split
    silent_intervals = librosa.effects.split(audio_data, top_db=15)

    # Filter silent intervals based on minimum duration
    long_silent_intervals = [interval for interval in silent_intervals if librosa.get_duration(y=audio_data[interval[0]:interval[1]]) >= min_long_silence_duration]

    # Calculate total duration of long silence and total duration of audio
    total_long_silence_duration = sum(librosa.get_duration(y=audio_data[interval[0]:interval[1]]) for interval in long_silent_intervals)
    total_duration = librosa.get_duration(y=audio_data)

    # Calculate Silence Ratio
    if total_duration > 0:
        silence_ratio = total_long_silence_duration / total_duration
        res=f"Silence Ratio: {silence_ratio:.2%}"
    else:
        res = "No audio found or duration is 0."

    return res



def transcribe(path):
    vb = VoiceBot(api_key="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")
    # audiofilepath = r"files\sample_call_1.mp3"
    audiofilepath = path
    transcript = vb.transcribe(audiofilepath) 
    # print(transcript)
    return transcript



def calculate_aht(zip_file_path):
    total_duration = 0
    total_calls = 0

    # Iterate over each audio file in the extracted folder
    for filename in os.listdir('files'):
        if filename.endswith('.mp3'):
            # Load audio file using pydub
            audio = AudioSegment.from_mp3(os.path.join('temp', filename))
            # Calculate duration in milliseconds
            duration = len(audio)
            total_duration += duration
            total_calls += 1

    # Calculate average handle time
    if total_calls > 0:
        average_handle_time = total_duration / total_calls
        # Convert milliseconds to seconds
        average_handle_time_seconds = average_handle_time / 1000
        return average_handle_time_seconds
    else:
        return 0
    
def ovr_r():
    # Initialize count of calls exceeding the optimal duration
    num_overcalls = 0
    total_calls = 0

    # Iterate over extracted audio files
    for file_name in os.listdir('files'):
        if file_name.endswith('.mp3'):  # Assuming audio files are in .mp3 format
            audio_file_path = os.path.join('files', file_name)

            # Load audio file and calculate its duration
            audio_data, _ = librosa.load(audio_file_path, sr=None)
            duration = librosa.get_duration(y=audio_data)

            # Check if the call duration exceeds the optimal duration
            if duration > 30:
                num_overcalls += 1

            total_calls += 1

    # Calculate overcall rate
    if total_calls > 0:
        overcall_rate = (num_overcalls / total_calls) * 100
        res = f"Overcall Rate: {overcall_rate:.2f}%"
    else:
        res = "No audio files found in the zip."

    return res

def chat(path):
    API_KEY = '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'
    API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

    def send_message(message):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(API_KEY)
        }
        data = {
            'model': 'gpt-3.5-turbo',  # Specify the model to use
            'messages': [{'role': 'user', 'content': message}],
        }
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return 'Error: {}'.format(response.text)
    prompt = """
First Call Resolution (FCR): Analyze the text provided and identify whether it is their first interaction or not. Indicates the percentage of calls resolved on the first interaction, showcasing the agent's ability to solve issues efficiently without follow-up 

Call Resolution Rate: Analyze the text provided and identify whether the  issue is resolved or not. The percentage of calls that result in the caller's issue being resolved, indicating the effectiveness of the agents' problem-solving skills.   

Call Transfer Rate: Analyze the text provided and identify whether the call is transfered or not.Measures how often calls are transferred to another agent or department, which can indicate the need for better first-contact resolution or agent training.

Error Rate: Analyze the text provided and identify The frequency of errors made by agents during calls, such as providing incorrect information or failing to follow proper protocols. check for the information is correct as per the airline travel.If it is not correct reduce the percentage.

Provide the answers in a way clear and short way in a single sentence without commas.
"""
    prompt2 = """
            First Call Resolution (FCR): Analyze the text provided and identify whether it is their first interaction or not.   

            Call Resolution Rate: Analyze the text provided and identify whether the  issue is resolved or not.

            Call Transfer Rate: Analyze the text provided and identify whether the call is transfered or not.
            Provide the answers in the below format whether it is 'YES' or 'NO':
            ['\First Call Resolution','\Call Resolution Rate','Call Transfer Rate:']. Provide the requested answer alone . No need of extra content
        """
    transcript = transcribe(path)
    result = prompt+"the conversation starts here\n"+transcript
    result2 = prompt2+"the conversation starts here\n"+transcript
    response = send_message(result)
    response2 = send_message(result2)
    # return eval(response)
    return response,response2

def wr_csv(filename,data,filep):
    csv_file_path = filep

    # Open the CSV file in append mode
    with open(csv_file_path, 'a',newline='') as csvfile:
        
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        
        # Write the data to the CSV file
        d = [filename]+[data] 
        csv_writer.writerow(d)

def process():
    folder_path = "files"

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            # Construct the full path to the audio file
            audio_file_path = os.path.join(folder_path, filename)
            
            # Perform chat
            chat_r1,chat_r2 = chat(audio_file_path)

            wr_csv(filename[:-4],chat_r1,"data.csv")
            wr_csv(filename[:-4],chat_r2,"vis.csv")



# def visualize():

    
#     csv_file_path = "data.csv"

#     # Define column names
#     column_names = ["Call_id", "FCR", "CRR", "CTR"]

#     # Read the CSV file into a DataFrame with specified column names
#     df = pd.read_csv(csv_file_path, names=column_names)

#     st.write(df)
#     st.dataframe(df)
#     columns_to_plot = [col for col in df.columns if col != 'Call_id']

#     # Initialize a list to store individual donut charts
#     charts = []

#     # Create a donut chart for each column
#     for col in columns_to_plot:
#         # Count the occurrences of each category in the column
#         col_counts = df[col].value_counts().reset_index()
#         col_counts.columns = [col, 'Count']
        
#         # Create a donut chart for the current column
#         chart = alt.Chart(col_counts).mark_donut().encode(
#             color=alt.Color(col, legend=None),
#             tooltip=[col, 'Count']
#         ).transform_calculate(
#             percent="datum.Count / sum(datum.Count)",
#             angle="2 * pi * datum.Count / sum(datum.Count)"
#         ).transform_filter(
#             alt.datum.Count > 0
#         ).properties(
#             width=200,
#             height=200,
#             title=f'{col} Distribution'
#         ).configure_mark(
#             angle=180
#         )
        
#         charts.append(chart)

#     # Combine all donut charts into a single row
#     combined_chart = alt.hconcat(*charts)

#     return combined_chart
        