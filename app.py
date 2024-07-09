from fastapi import FastAPI
from database import engine, Base
from routers import users, profiles, text_entries
import models  # This imports all models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(profiles.router, prefix="/api/v1", tags=["profiles"])
app.include_router(text_entries.router, prefix="/api/v1", tags=["text_entries"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# from fastapi import FastAPI
# from routers import (
#     users,
#     profiles,
#     text_entries,
#     audio,
#     voice_clones,
#     feedback,
#     settings,
#     api_usage,
#     error_logs,
#     sessions,
#     usage_history,
# )

# app = FastAPI()

# app.include_router(users.router, prefix="/api/v1", tags=["users"])
# app.include_router(profiles.router, prefix="/api/v1", tags=["profiles"])
# app.include_router(text_entries.router, prefix="/api/v1", tags=["text_entries"])

# # app.include_router(audio.router)
# # app.include_router(voice_clones.router)
# # app.include_router(feedback.router)
# # app.include_router(settings.router)
# # app.include_router(api_usage.router)
# # app.include_router(error_logs.router)
# # app.include_router(sessions.router)
# # app.include_router(usage_history.router)

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import Config
# from models import db, User
# from api.auth import auth_bp
# from api.tts import tts_bp

# app = Flask(__name__)
# app.config.from_object(Config)

# db.init_app(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "auth.login"


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# # Register Blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(tts_bp)

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, port=5001)
