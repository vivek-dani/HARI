import streamlit as st
import requests
import os
import tempfile
import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import io
from pydub import AudioSegment
import time
import base64
import queue
import json
from location_component import google_maps_component, process_location
import aws_api
import rag_api
from os.path import exists, join
import constants as cnst

# Set page configuration
st.set_page_config(
    page_title="HARI: Human's Assistant for Real-time Interventions",
    page_icon="🎵",
    layout="wide"
)

# Server URL
SERVER_URL = "http://localhost:5000"

# Function to check if server is running
def is_server_running():
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# Function to play audio from bytes
def play_audio(audio_bytes):
    # Create a base64 encoded audio string
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

# Function to handle audio recording
def process_audio(audio_file):
    text = aws_api.get_diarized_transcript(audio_file)
    print(f"Transcription: {text}")
    file_path_txt, ans = rag_api.answer_frm_rag(text)

    if exists(file_path_txt):
        video_file = open(file_path_txt, "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)
        audio_file = aws_api.tts(ans)
        autoplay_audio(audio_file)
        
    else:
        audio_file = aws_api.tts("I don't know, sorry")
        autoplay_audio(audio_file)

# Function to handle date-time selection
def process_datetime(selected_datetime):
    time_dict, time_evidence = rag_api.get_actions()
    print(time_dict)
    print(selected_datetime)
    if selected_datetime in time_dict:
        audio_file = aws_api.tts("Hey, I thought I might remind you to " + ' '.join(time_dict[selected_datetime]))
        autoplay_audio(audio_file)

        for video_name in time_evidence[selected_datetime]:
            video_file_path = join(cnst.video_path, video_name+".mp4")
            if exists(video_file_path):
                video_file = open(video_file_path, "rb")
                video_bytes = video_file.read()
                st.video(video_bytes)


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
         
            md,
            unsafe_allow_html=True,
        )

# Main app
def main():

    os.environ["OPENAI_API_KEY"]=""
    os.environ["OPENAI_API_BASE"]=""
    os.environ["AWS_PROFILE"] = cnst.profile_name
    st.title("HARI: Human's Assistant for Real-time Interventions")
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Audio Input", "DateTime Input", "Location Input"])
    
    # Audio Input Tab
    with tab1:
        st.header("Audio Input")
        audio_value = st.audio_input("Provide a voice command")
        
        if audio_value:
            st.audio(audio_value)
            with open("uploads/recorded_audio.wav", "wb") as f:
                f.write(audio_value.getbuffer())
                st.write("Command received...")
                #autoplay_audio("uploads/recorded_audio.wav")
        
                response_audio = process_audio("uploads/recorded_audio.wav")
                st.write(response_audio)
                    
    # DateTime Input Tab
    with tab2:
        st.header("DateTime Input")
        st.write("Mock current date and time.")
        selected_date = st.date_input("Select a date", datetime.date.today())
        selected_time = st.time_input("Select a time", datetime.time(12, 0))
        
        selected_datetime = datetime.datetime.combine(selected_date, selected_time)
        st.write(f"Current mocked: {selected_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("Mock DateTime"):
            process_datetime(str(selected_datetime))
    
    # Location Input Tab
    with tab3:
        st.header("Location Input")
        from streamlit_geolocation import streamlit_geolocation
        location = streamlit_geolocation()
        st.write(location)
        response_audio = process_location(location)
       
if __name__ == "__main__":
    main()
