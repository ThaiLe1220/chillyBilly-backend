from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
import requests
import os
import uuid
from datetime import datetime
from models_old import db, Audio

tts_bp = Blueprint("tts", __name__)


@tts_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@tts_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    text = request.form["text"]
    lang = request.form["lang"]
    payload = {"text": text, "lang": lang}
    response = requests.post(
        "https://face-swap.12pmtech.link//generate_audio", json=payload, timeout=60
    )
    if response.status_code == 200:
        response_data = response.json()
        save_metadata(response_data["file_url"], text, lang, current_user.id)
        return render_template("result.html", file_url=response_data["file_url"])
    else:
        return jsonify({"error": response.json().get("error")}), 400


def save_metadata(file_url, text, lang, user_id):
    session_id = str(uuid.uuid4())
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = file_url.split("/")[-1]

    new_audio = Audio(
        filename=filename,
        file_url=file_url,
        text=text,
        lang=lang,
        session_id=session_id,
        datetime=current_datetime,
        user_id=user_id,
    )
    db.session.add(new_audio)
    db.session.commit()


@tts_bp.route("/my_audios")
@login_required
def my_audios():
    audios = Audio.query.filter_by(user_id=current_user.id).all()
    return render_template("my_audios.html", audios=audios)
