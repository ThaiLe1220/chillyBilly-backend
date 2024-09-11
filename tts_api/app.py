# ./tts_api/app.py

from flask import Flask, request
from services.voice_service import VoiceService
from services.audio_service import AudioService

app = Flask(__name__)

BASE_VOICES_DIR = "tts_api/tortoise/voices"
BASE_OUTPUT_DIR = "output"
MIN_AUDIO_LENGTH = 15

voice_service = VoiceService(app, BASE_VOICES_DIR, MIN_AUDIO_LENGTH)
audio_service = AudioService(BASE_OUTPUT_DIR, BASE_VOICES_DIR)


@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    return audio_service.generate_audio(request.json)


@app.route("/download/<user_type>/<user_id>/<filename>", methods=["GET"])
def download_audio(user_type, user_id, filename):
    return audio_service.download_audio(user_type, user_id, filename)


@app.route("/delete_audio/<user_type>/<user_id>/<filename>", methods=["DELETE"])
def delete_audio(user_type, user_id, filename):
    return audio_service.delete_audio(user_type, user_id, filename)


@app.route("/delete_all_user_audio/<user_type>/<user_id>", methods=["DELETE"])
def delete_all_user_audio(user_type, user_id):
    return audio_service.delete_all_user_audio(user_type, user_id)


@app.route("/delete_all_audio", methods=["DELETE"])
def delete_all_audio():
    return audio_service.delete_all_audio()


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
