import requests


# URL of the backend endpoint
BACKEND_URL = "http://127.0.0.1:5001/upload"  # Updated to port 5001

# Path to the audio file you want to upload
AUDIO_FILE_PATH = "test_files/test_positive.m4a"

# Send the file as a POST request
with open(AUDIO_FILE_PATH, "rb") as audio_file:
    files = {"file": audio_file}
    response = requests.post(BACKEND_URL, files=files)

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")