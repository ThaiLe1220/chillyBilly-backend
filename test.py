import requests
import os
import uuid
from datetime import datetime

# Define the API endpoints
base_url = "http://127.0.0.1:5000"
generate_audio_endpoint = f"{base_url}/generate_audio"

# Define the text and languages
texts = [
    {"text": "Hello, world!", "lang": "en"},
    {"text": "Xin chào, thế giới!", "lang": "vi"},
]

# Directory to save the metadata file
output_dir = "."


def generate_audio(text, lang):
    # Create the payload
    payload = {"text": text, "lang": lang}

    # Send the POST request to generate audio
    response = requests.post(generate_audio_endpoint, json=payload)
    response_data = response.json()

    if response.status_code == 200:
        print(f"Audio generated successfully: {response_data['file_url']}")
        return response_data["file_url"]
    else:
        print(f"Error: {response_data['error']}")
        return None


def save_metadata(file_url, text, lang):
    session_id = str(uuid.uuid4())
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = file_url.split("/")[-1]

    # Metadata string
    metadata = f"Session ID: {session_id}\n"
    metadata += f"Date and Time: {current_datetime}\n"
    metadata += f"Audio Transcript: {text}\n"
    metadata += f"Language: {lang}\n"
    metadata += f"Audio Name: {filename}\n"
    metadata += f"Download Link: {file_url}\n"
    metadata += "-" * 40 + "\n"

    # Write metadata to file
    with open(os.path.join(output_dir, "audio_metadata.txt"), "a") as file:
        file.write(metadata)

    print(f"Metadata saved for audio: {filename}")


def main():
    # Generate and save metadata for each text
    for item in texts:
        file_url = generate_audio(item["text"], item["lang"])
        if file_url:
            save_metadata(file_url, item["text"], item["lang"])


if __name__ == "__main__":
    main()
