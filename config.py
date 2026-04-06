import os
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

IMAGE_SOURCE = os.getenv("IMAGE_SOURCE", "unsplash")

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

STABLE_DIFFUSION_API_URL = os.getenv("STABLE_DIFFUSION_API_URL")
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")

NICHE = os.getenv("NICHE", "lifestyle")
POSTING_TIMES = os.getenv("POSTING_TIMES", "09:00,18:00")

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "60"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

USE_AI_IMAGES = os.getenv("USE_AI_IMAGES", "false").lower() == "true"

AI_IMAGE_MODELS = {
    "flux": "flux (default, high quality)",
    "turbo": "turbo (faster generation)",
}
