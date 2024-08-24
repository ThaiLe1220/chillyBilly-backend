# ./tts_api.py/download_models.py

import os
import sys

# Add the parent directory to the Python path to import the utils module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise.models.utils import MODELS, get_model_path, MODELS_DIR


def download_all_models():
    print("Checking and downloading Tortoise TTS models...")
    for model_name in MODELS.keys():
        try:
            model_path = get_model_path(model_name)
            print(f"Model {model_name} is available at {model_path}")
        except Exception as e:
            print(f"Error downloading {model_name}: {str(e)}")
    print("All models have been checked and downloaded if necessary.")


if __name__ == "__main__":
    download_all_models()
