# ./tts_api.py/download_models.py

import os
import sys

# Add the parent directory to the Python path to import the utils module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise.models.utils import MODELS, get_model_path, MODELS_DIR


def download_all_models():
    print("Checking Tortoise TTS models...")
    all_models_exist = True
    for model_name in MODELS.keys():
        model_path = os.path.join(MODELS_DIR, model_name)
        if os.path.exists(model_path):
            print(f"Model {model_name} already exists at {model_path}")
        else:
            all_models_exist = False
            print(f"Model {model_name} does not exist. It will be downloaded.")

    if all_models_exist:
        print("All models already exist. No downloads necessary.")
    else:
        print("Downloading missing models...")
        for model_name in MODELS.keys():
            try:
                model_path = get_model_path(model_name)
                print(f"Model {model_name} is now available at {model_path}")
            except Exception as e:
                print(f"Error downloading {model_name}: {str(e)}")

    print("All models have been checked and downloaded if necessary.")


if __name__ == "__main__":
    download_all_models()
