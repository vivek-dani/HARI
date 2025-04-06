# Streamlit HARI: Human's Assistant for Real-time Interventions

This is a Streamlit web application that:
1. Takes audio input from a microphone and plays an MP3 file received from a server in response
2. Takes a date-time input from a calendar box and plays an MP3 file received from a server in response
3. Takes a location input using Google Maps and plays an MP3 file received from a server in response

## Project Structure

```
web_server/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Dependencies
├── static/
│   ├── mp3/                   # Directory for sample MP3 files
│   ├── js/
│   │   ├── maps.js            # JavaScript for Google Maps functionality
│   │   └── streamlit_component.js  # JavaScript for Streamlit component
│   └── location.html          # HTML template for Google Maps
└── uploads/                   # Directory for uploaded audio files
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Streamlit App

Open another terminal and run:

```bash
streamlit run app.py
```

This will start the Streamlit app and open it in your default web browser.

## Using the App

### Audio Input

1. Navigate to the "Audio Input" tab
2. Click the "PLAY" button to begin recording audio from your microphone
3. Speak into your microphone
4. Click "PAUSE" when you're done recording
5. Click the "Process Audio Recording" button
6. The server will process your audio and return an MP3 file, which will be played automatically

### DateTime Input

1. Navigate to the "DateTime Input" tab
2. Select a date using the date picker
3. Select a time using the time picker
4. Click the "Mock DateTime" button
5. The server will process your date-time selection and return an MP3 file, which will be played automatically
