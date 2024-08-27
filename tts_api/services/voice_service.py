# ./tts_api/services/voice_service.py

import os
import shutil
from flask import jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment


class VoiceService:
    def __init__(self, app, base_voices_dir, min_audio_length):
        self.app = app
        self.BASE_VOICES_DIR = base_voices_dir
        self.MIN_AUDIO_LENGTH = min_audio_length

    def add_voice(self, request):
        try:
            self.app.logger.info("Received request to add voice")
            if "file" not in request.files:
                self.app.logger.error("No file part in the request")
                return jsonify({"error": "No file part"}), 400

            file = request.files["file"]
            user_id = request.form.get("user_id")
            voice_name = request.form.get("voice_name")

            self.app.logger.info(
                "Received file: %s, Content-Type: %s, user_id: %s, voice_name: %s",
                file.filename,
                file.content_type,
                user_id,
                voice_name,
            )

            if not file or file.filename == "":
                self.app.logger.error("No selected file")
                return jsonify({"error": "No selected file"}), 400

            if not user_id or not voice_name:
                self.app.logger.error("User ID and voice name are required")
                return jsonify({"error": "User ID and voice name are required"}), 400

            if not self.is_valid_user_id(user_id):
                self.app.logger.error("Invalid user ID: %s", user_id)
                return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

            user_voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id, voice_name)
            os.makedirs(user_voice_dir, exist_ok=True)
            self.app.logger.info("Created user voice directory: %s", user_voice_dir)

            temp_filename = secure_filename(file.filename)
            temp_file_path = os.path.join(user_voice_dir, temp_filename)
            file.save(temp_file_path)
            self.app.logger.info("Saved temporary file: %s", temp_file_path)

            audio = AudioSegment.from_file(temp_file_path)
            self.app.logger.info(
                "Loaded audio file, length: %s seconds", len(audio) / 1000
            )

            if len(audio) < self.MIN_AUDIO_LENGTH * 1000:
                os.remove(temp_file_path)
                self.app.logger.error(
                    "Audio file too short: %s seconds", len(audio) / 1000
                )
                return (
                    jsonify(
                        {
                            "error": f"Audio file must be at least {self.MIN_AUDIO_LENGTH} seconds long"
                        }
                    ),
                    400,
                )

            part_length = len(audio) // 3
            part1 = audio[:part_length]
            part2 = audio[part_length : 2 * part_length]
            part3 = audio[2 * part_length :]

            part1.export(os.path.join(user_voice_dir, "1.wav"), format="wav")
            part2.export(os.path.join(user_voice_dir, "2.wav"), format="wav")
            part3.export(os.path.join(user_voice_dir, "3.wav"), format="wav")
            self.app.logger.info("Exported audio parts successfully")

            os.remove(temp_file_path)
            self.app.logger.info("Removed temporary file: %s", temp_file_path)

            response = {
                "message": "Voice sample uploaded and split successfully",
                "user_id": user_id,
                "voice_name": voice_name,
                "parts": ["1.wav", "2.wav", "3.wav"],
                "total_length": len(audio) / 1000,
            }
            self.app.logger.info("Voice addition successful: %s", response)
            return jsonify(response), 201

        except Exception as e:
            self.app.logger.error(
                "Unexpected error in add_voice: %s", str(e), exc_info=True
            )
            return jsonify({"error": "An unexpected error occurred"}), 500

    def get_user_voices(self, user_id):
        user_voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id)
        if not os.path.exists(user_voice_dir):
            return []
        return [
            d
            for d in os.listdir(user_voice_dir)
            if os.path.isdir(os.path.join(user_voice_dir, d))
        ]

    def list_voices(self, user_id):
        if not self.is_valid_user_id(user_id):
            return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

        voices = self.get_user_voices(user_id)
        voice_details = []
        for voice in voices:
            voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id, voice)
            parts = [f for f in os.listdir(voice_dir) if f.endswith(".wav")]
            total_length = sum(
                AudioSegment.from_wav(os.path.join(voice_dir, part)).duration_seconds
                for part in parts
            )
            voice_details.append(
                {"name": voice, "parts": parts, "total_length": total_length}
            )

        return jsonify({"user_id": user_id, "voices": voice_details})

    def delete_voice(self, user_id, voice_name):
        if not self.is_valid_user_id(user_id):
            return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

        voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id, voice_name)
        if os.path.exists(voice_dir):
            try:
                shutil.rmtree(voice_dir)
                return (
                    jsonify({"message": f"Voice '{voice_name}' deleted successfully"}),
                    200,
                )
            except Exception as e:
                return jsonify({"error": f"Failed to delete voice: {str(e)}"}), 500
        else:
            return jsonify({"error": "Voice not found"}), 404

    def delete_all_user_voices(self, user_id):
        if not self.is_valid_user_id(user_id):
            return jsonify({"error": "Invalid user ID. Must be alphanumeric"}), 400

        user_voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id)
        if os.path.exists(user_voice_dir):
            try:
                shutil.rmtree(user_voice_dir)
                os.makedirs(user_voice_dir)
                return (
                    jsonify(
                        {
                            "message": f"All voices for user '{user_id}' deleted successfully"
                        }
                    ),
                    200,
                )
            except Exception as e:
                return (
                    jsonify({"error": f"Failed to delete user voices: {str(e)}"}),
                    500,
                )
        else:
            return jsonify({"error": "User voice directory not found"}), 404

    def delete_all_custom_voices(self):
        try:
            deleted_count = 0
            for user_id in os.listdir(self.BASE_VOICES_DIR):
                if user_id.isdigit():
                    user_voice_dir = os.path.join(self.BASE_VOICES_DIR, user_id)
                    if os.path.isdir(user_voice_dir):
                        shutil.rmtree(user_voice_dir)
                        os.makedirs(user_voice_dir)
                        deleted_count += 1

            if deleted_count > 0:
                return (
                    jsonify(
                        {
                            "message": f"Custom voices deleted for {deleted_count} numeric user(s) successfully"
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify({"message": "No custom voices found for numeric user IDs"}),
                    200,
                )
        except Exception as e:
            return jsonify({"error": f"Failed to delete custom voices: {str(e)}"}), 500

    @staticmethod
    def is_valid_user_id(user_id):
        import re

        return re.match(r"^[a-zA-Z0-9]+$", user_id) is not None
