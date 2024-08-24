import os
import re
import requests
import progressbar
from dotenv import load_dotenv

try:
    import gdown
except ImportError:
    raise ImportError(
        "Sorry, gdown is required in order to download the new BigVGAN vocoder.\n"
        "Please install it with `pip install gdown` and try again."
    )
from urllib import request

import progressbar

load_dotenv()

D_STEM = "https://drive.google.com/uc?id="

DEFAULT_MODELS_DIR = os.path.join(
    os.path.expanduser("~"), ".cache", "tortoise", "models"
)
MODELS_DIR = os.environ.get("TORTOISE_MODELS_DIR", DEFAULT_MODELS_DIR)
MODELS = {
    "autoregressive.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/autoregressive.pth",
    "autoregressive_vi.pth": "https://huggingface.co/Eugenememe/vietnamese_langugage_gpt/resolve/main/autoregressive_vi.pth?download=true",
    "classifier.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/classifier.pth",
    "clvp2.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/clvp2.pth",
    "cvvp.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/cvvp.pth",
    "diffusion_decoder.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/diffusion_decoder.pth",
    "vocoder.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/vocoder.pth",
    "rlg_auto.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/rlg_auto.pth",
    "rlg_diffuser.pth": "https://huggingface.co/jbetker/tortoise-tts-v2/resolve/main/.models/rlg_diffuser.pth",
    # these links are from the nvidia gdrive
    "bigvgan_base_24khz_100band_g.pth": "https://drive.google.com/uc?id=1_cKskUDuvxQJUEBwdgjAxKuDTUW6kPdY",
    "bigvgan_24khz_100band_g.pth": "https://drive.google.com/uc?id=1wmP_mAs7d00KHVfVEl8B5Gb72Kzpcavp",
}


pbar = None
HF_TOKEN = os.environ.get("HF_TOKEN")


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def download_file(url, filename):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if "huggingface.co" in url else {}
    with requests.get(url, stream=True, headers=headers, timeout=30) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        block_size = 8192

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    show_progress(1, len(chunk), total_size)


def download_models(specific_models=None):
    """
    Call to download all the models that Tortoise uses.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    for model_name, url in MODELS.items():
        if specific_models is not None and model_name not in specific_models:
            continue
        model_path = os.path.join(MODELS_DIR, model_name)
        if os.path.exists(model_path):
            continue
        print(f"Downloading {model_name} from {url}...")
        if D_STEM in url:
            gdown.download(url, model_path, quiet=False)
        elif "huggingface.co" in url:
            download_file(url, model_path)
        else:
            request.urlretrieve(url, model_path)
        print("Done.")


def get_model_path(model_name, models_dir=MODELS_DIR):
    """
    Get path to given model, download it if it doesn't exist.
    """
    # Check for exact match first
    if model_name in MODELS:
        model_path = os.path.join(models_dir, model_name)
    else:
        # Check for custom language models
        if model_name in MODELS:
            model_path = os.path.join(models_dir, model_name)
        else:
            raise ValueError(f"Model {model_name} not found in available models.")

    if not os.path.exists(model_path) and models_dir == MODELS_DIR:
        download_models([model_name])
    return model_path
