from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    audios = db.relationship("Audio", backref="owner")


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    file_url = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    lang = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
