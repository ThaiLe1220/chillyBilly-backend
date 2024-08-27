""" ./tts_api/app.py"""

import time
from flask import Flask, request, jsonify, send_from_directory
import torchaudio
from tortoise.api import TextToSpeech
import os
import uuid
from queue import Queue
import threading
from tortoise.utils.audio import load_voice
import re
import librosa
import shutil
from werkzeug.utils import secure_filename
from pydub import AudioSegment

from services.voice_service import VoiceService

app = Flask(__name__)

BASE_VOICES_DIR = "tts_api/tortoise/voices"
MIN_AUDIO_LENGTH = 25

voice_service = VoiceService(app, BASE_VOICES_DIR, MIN_AUDIO_LENGTH)


@app.route("/add_voice", methods=["POST"])
def add_voice():
    return voice_service.add_voice(request)


@app.route("/list_voices/<user_id>", methods=["GET"])
def list_voices(user_id):
    return voice_service.list_voices(user_id)


@app.route("/delete_voice/<user_id>/<voice_name>", methods=["DELETE"])
def delete_voice(user_id, voice_name):
    return voice_service.delete_voice(user_id, voice_name)


@app.route("/delete_all_user_voices/<user_id>", methods=["DELETE"])
def delete_all_user_voices(user_id):
    return voice_service.delete_all_user_voices(user_id)


@app.route("/delete_all_custom_voices", methods=["DELETE"])
def delete_all_custom_voices():
    return voice_service.delete_all_custom_voices()


# Create a queue to handle requests
request_queue = Queue()


def generate_speech(tts_model, text, voice_name, preset, output_file):
    """Generate speech using the specified voice and text."""
    start_time = time.time()
    voice_samples, conditioning_latents = load_voice(voice_name)
    gen = tts_model.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=preset,
    )
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    end_time = time.time()
    generated_time = end_time - start_time

    # Calculate audio duration and wavelength
    audio_duration = librosa.get_duration(filename=output_file)
    y, sr = librosa.load(output_file)
    wavelength = len(y) / sr

    return output_file, generated_time, audio_duration, wavelength


def is_valid_user_id(user_id):
    return re.match(r"^[a-zA-Z0-9]+$", user_id) is not None


# Function to process requests in the queue
def process_queue():
    while True:
        tts_model, text, voice_name, preset, output_file, result_queue = (
            request_queue.get()
        )
        try:
            output_file, generated_time, audio_duration, wavelength = generate_speech(
                tts_model, text, voice_name, preset, output_file
            )
            result_queue.put((output_file, generated_time, audio_duration, wavelength))
        finally:
            request_queue.task_done()


# Load TextToSpeech models
tts = TextToSpeech()
tts_vi = TextToSpeech(lang="vi")

DEFAULT_VOICES = [
    "default_en_male",
    "default_en_female",
    "default_vi_male",
    "default_vi_female",
]
BASE_OUTPUT_DIR = "output"

# Start a thread to process the queue
threading.Thread(target=process_queue, daemon=True).start()


@app.route("/health")
def health():
    return "OK", 200


@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    data = request.json
    text = data.get("text")
    lang = data.get("lang", "vi")
    voice_name = data.get("voice_name", "default_vi_female")
    voice_new_name = ""
    user_id = data.get("user_id", "anonymous")
    user_type = data.get("user_type", "guest")
    preset = data.get("preset", "ultra_fast")

    print(
        f"Processing request - Text: {text[:50]}..., Lang: {lang}, Voice: {voice_name}, User ID: {user_id}, User Type: {user_type}, Preset: {preset}"
    )

    if not text or not lang:
        return jsonify({"error": "Please provide both text and lang"}), 400

    if user_type not in ["guest", "user"]:
        return jsonify({"error": "Invalid user type. Must be 'guest' or 'user'"}), 400

    if not is_valid_user_id(user_id):
        return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

    if lang == "vi":
        tts_model = tts_vi
    else:
        tts_model = tts

    # Check if it's a user-uploaded voice
    if voice_name not in DEFAULT_VOICES:
        user_voice_dir = os.path.join(BASE_VOICES_DIR, user_id, voice_name)
        if os.path.exists(user_voice_dir):
            voice_new_name = os.path.join(user_id, voice_name)
        else:
            return jsonify({"error": "Requested custom voice not found"}), 404
    else:
        voice_new_name = voice_name

    # Create user-specific output directory
    user_output_dir = os.path.join(BASE_OUTPUT_DIR, user_type, user_id)
    os.makedirs(user_output_dir, exist_ok=True)

    # Generate a unique filename
    timestamp = int(time.time())
    filename = f"{timestamp}_{voice_name}_{uuid.uuid4().hex[:8]}.wav"
    output_file = os.path.join(user_output_dir, filename)

    result_queue = Queue()
    request_queue.put(
        (tts_model, text, voice_new_name, preset, output_file, result_queue)
    )

    # Wait for the result
    output_file, generated_time, audio_duration, wavelength = result_queue.get()

    download_url = request.url_root + f"download/{user_type}/{user_id}/{filename}"
    delete_url = request.url_root + f"delete_audio/{user_type}/{user_id}/{filename}"
    file_size = os.path.getsize(output_file)

    response_data = {
        "message": "Audio generated successfully",
        "download_url": download_url,
        "delete_url": delete_url,
        "audio_name": filename,
        "audio_size": file_size,
        "audio_path": output_file,
        "generation_time": generated_time,
        "audio_duration": audio_duration,
        "audio_wavelength": wavelength,
        "user_type": user_type,
        "user_id": user_id,
        "voice_name": voice_name,
        "language": lang,
        "preset": preset,
        "timestamp": timestamp,
        "text_length": len(text),
        "mime_type": "audio/wav",
        "sample_rate": 24000,
    }

    return jsonify(response_data)


@app.route("/download/<user_type>/<user_id>/<filename>", methods=["GET"])
def download_audio(user_type, user_id, filename):
    directory = os.path.join(BASE_OUTPUT_DIR, user_type, user_id)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/delete_audio/<user_type>/<user_id>/<filename>", methods=["DELETE"])
def delete_audio(user_type, user_id, filename):
    file_path = os.path.join(BASE_OUTPUT_DIR, user_type, user_id, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({"message": "Audio file deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete audio file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Audio file not found"}), 404


@app.route("/delete_all_user_audio/<user_type>/<user_id>", methods=["DELETE"])
def delete_all_user_audio(user_type, user_id):
    user_dir = os.path.join(BASE_OUTPUT_DIR, user_type, user_id)
    if os.path.exists(user_dir):
        try:
            # Delete all files in the user's directory
            for filename in os.listdir(user_dir):
                file_path = os.path.join(user_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return (
                jsonify(
                    {
                        "message": f"All audio files for user {user_id} deleted successfully"
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": f"Failed to delete audio files: {str(e)}"}), 500
    else:
        return jsonify({"error": "User directory not found"}), 404


@app.route("/delete_all_audio", methods=["DELETE"])
def delete_all_audio():
    try:
        # Delete all subdirectories and files in the base output directory
        for user_type in os.listdir(BASE_OUTPUT_DIR):
            user_type_path = os.path.join(BASE_OUTPUT_DIR, user_type)
            if os.path.isdir(user_type_path):
                shutil.rmtree(user_type_path)

        # Recreate the base structure
        os.makedirs(os.path.join(BASE_OUTPUT_DIR, "guest"), exist_ok=True)
        os.makedirs(os.path.join(BASE_OUTPUT_DIR, "user"), exist_ok=True)

        return jsonify({"message": "All audio files deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete all audio files: {str(e)}"}), 500


# ... (rest of the existing code)

if __name__ == "__main__":
    # Start the queue processing thread
    threading.Thread(target=process_queue, daemon=True).start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=8080, debug=False)
