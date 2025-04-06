# Streamlit HARI: Human's Assistant for Real-time Interventions

This is a Streamlit web application that:
1. Takes audio input from a microphone and plays an MP3 file received from a server in response
2. Takes a date-time input from a calendar box and plays an MP3 file received from a server in response
3. Takes a location input using Google Maps and plays an MP3 file received from a server in response

## Project Structure

```
web_server/
├── app.py                     # Main Streamlit application
├── server.py                  # Flask server to handle requests and return MP3 files
├── location_component.py      # Custom Streamlit component for Google Maps integration
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

### 2. Start the Flask Server

Open a terminal and run:

```bash
python server.py
```

You should see a message indicating that the server is running on http://localhost:5000.

### 3. Start the Streamlit App

Open another terminal and run:

```bash
streamlit run app.py
```

This will start the Streamlit app and open it in your default web browser.

## Using the App

### Audio Input

1. Navigate to the "Audio Input" tab
2. Click the "START" button to begin recording audio from your microphone
3. Speak into your microphone
4. Click "STOP" when you're done recording
5. Click the "Process Audio Recording" button
6. The server will process your audio and return an MP3 file, which will be played automatically

### DateTime Input

1. Navigate to the "DateTime Input" tab
2. Select a date using the date picker
3. Select a time using the time picker
4. Click the "Process DateTime" button
5. The server will process your date-time selection and return an MP3 file, which will be played automatically

### Location Input

1. Navigate to the "Location Input" tab
2. Enter your Google Maps API key (you can get one from the [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/))
3. Search for a location using the search box or by clicking on the map
4. Once a location is selected, its details will be displayed
5. Click the "Process Location" button
6. The server will process your location selection and return an MP3 file, which will be played automatically

#### Getting a Google Maps API Key

To use the Location Input feature, you need a Google Maps API key with the following APIs enabled:
- Maps JavaScript API
- Places API

Follow these steps to get an API key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Library"
4. Search for and enable the Maps JavaScript API and Places API
5. Go to "APIs & Services" > "Credentials"
6. Click "Create Credentials" > "API Key"
7. Copy the generated API key and use it in the app

## Notes

- The server creates dummy MP3 files for demonstration purposes. In a real application, you would replace these with actual MP3 files or generate them dynamically based on the input.
- The app checks if the server is running and displays the status in the sidebar. If the server is not running, you'll see an error message.



"""
# Check if server is running
server_status = "Running ✅" if is_server_running() else "Not Running ❌"
st.sidebar.write(f"Server Status: {server_status}")

if not is_server_running():
    st.sidebar.error("Please start the server by running: python server.py")
"""