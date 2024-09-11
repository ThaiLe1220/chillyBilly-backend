# ./tts_api/services/audio_service.py

import os
import time
import uuid
import threading
from queue import Queue
from flask import jsonify, send_from_directory
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
import torchaudio
import librosa
import shutil


class AudioService:
    def __init__(self, base_output_dir, base_voices_dir):
        self.tts = TextToSpeech()
        self.tts_vi = TextToSpeech(lang="vi")
        self.request_queue = Queue()
        self.BASE_OUTPUT_DIR = base_output_dir
        self.BASE_VOICES_DIR = base_voices_dir
        self.DEFAULT_VOICES = [
            "default_en_male",
            "default_en_female",
            "default_vi_male",
            "default_vi_female",
        ]

        # Start the queue processing thread
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        while True:
            tts_model, text, voice_name, preset, output_file, result_queue = (
                self.request_queue.get()
            )
            try:
                output_file, generated_time, audio_duration, wavelength = (
                    self.generate_speech(
                        tts_model, text, voice_name, preset, output_file
                    )
                )
                result_queue.put(
                    (output_file, generated_time, audio_duration, wavelength)
                )
            finally:
                self.request_queue.task_done()

    def generate_speech(self, tts_model, text, voice_name, preset, output_file):
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

        audio_duration = librosa.get_duration(filename=output_file)
        y, sr = librosa.load(output_file)
        wavelength = len(y) / sr

        return output_file, generated_time, audio_duration, wavelength

    def generate_audio(self, data):
        text = data.get("text")
        lang = data.get("lang", "vi")
        voice_name = data.get("voice_name", "default_vi_female")
        user_id = data.get("user_id", "anonymous")
        user_type = data.get("user_type", "guest")
        preset = data.get("preset", "ultra_fast")

        if not text or not lang:
            return jsonify({"error": "Please provide both text and lang"}), 400

        if user_type not in ["guest", "user"]:
            return (
                jsonify({"error": "Invalid user type. Must be 'guest' or 'user'"}),
                400,
            )

        if not self.is_valid_user_id(user_id):
            return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

        tts_model = self.tts_vi if lang == "vi" else self.tts

        voice_new_name = self.get_voice_path(user_id, voice_name)
        if not voice_new_name:
            return jsonify({"error": "Requested custom voice not found"}), 404

        user_output_dir = os.path.join(self.BASE_OUTPUT_DIR, user_type, user_id)
        os.makedirs(user_output_dir, exist_ok=True)

        timestamp = int(time.time())
        filename = f"{timestamp}_{voice_name}_{uuid.uuid4().hex[:8]}.wav"
        output_file = os.path.join(user_output_dir, filename)

        result_queue = Queue()
        self.request_queue.put(
            (tts_model, text, voice_new_name, preset, output_file, result_queue)
        )

        output_file, generated_time, audio_duration, wavelength = result_queue.get()

        file_size = os.path.getsize(output_file)

        response_data = {
            "message": "Audio generated successfully",
            "download_url": f"/download/{user_type}/{user_id}/{filename}",
            "delete_url": f"/delete_audio/{user_type}/{user_id}/{filename}",
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

    def download_audio(self, user_type, user_id, filename):
        directory = os.path.join(self.BASE_OUTPUT_DIR, user_type, user_id)
        return send_from_directory(directory, filename, as_attachment=True)

    def delete_audio(self, user_type, user_id, filename):
        file_path = os.path.join(self.BASE_OUTPUT_DIR, user_type, user_id, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return jsonify({"message": "Audio file deleted successfully"}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to delete audio file: {str(e)}"}), 500
        else:
            return jsonify({"error": "Audio file not found"}), 404

    def delete_all_user_audio(self, user_type, user_id):
        user_dir = os.path.join(self.BASE_OUTPUT_DIR, user_type, user_id)
        if os.path.exists(user_dir):
            try:
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
                return (
                    jsonify({"error": f"Failed to delete audio files: {str(e)}"}),
                    500,
                )
        else:
            return jsonify({"error": "User directory not found"}), 404

    def delete_all_audio(self):
        try:
            for user_type in os.listdir(self.BASE_OUTPUT_DIR):
                user_type_path = os.path.join(self.BASE_OUTPUT_DIR, user_type)
                if os.path.isdir(user_type_path):
                    shutil.rmtree(user_type_path)

            os.makedirs(os.path.join(self.BASE_OUTPUT_DIR, "guest"), exist_ok=True)
            os.makedirs(os.path.join(self.BASE_OUTPUT_DIR, "user"), exist_ok=True)

            return jsonify({"message": "All audio files deleted successfully"}), 200
        except Exception as e:
            return (
                jsonify({"error": f"Failed to delete all audio files: {str(e)}"}),
                500,
            )

    def get_voice_path(self, user_id, voice_name):
        if voice_name in self.DEFAULT_VOICES:
            return voice_name
        user_voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id, voice_name)
        return (
            os.path.join(user_id, voice_name)
            if os.path.exists(user_voice_dir)
            else None
        )

    @staticmethod
    def is_valid_user_id(user_id):
        import re

        return re.match(r"^[a-zA-Z0-9]+$", user_id) is not None
