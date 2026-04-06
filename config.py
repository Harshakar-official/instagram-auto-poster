import os
from dotenv import load_dotenv

load_dotenv()


def get_required(key: str, default: str = None) -> str:
    value = os.getenv(key, default)
    if not value or value.startswith("your_"):
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def get_optional(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def get_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


def get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


INSTAGRAM_USER_ID = get_optional("INSTAGRAM_USER_ID", "")
ACCESS_TOKEN = get_optional("ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID = get_optional("FACEBOOK_PAGE_ID", "")

HUGGINGFACE_TOKEN = get_optional("HUGGINGFACE_TOKEN", "")

IMAGE_SOURCE = get_optional("IMAGE_SOURCE", "unsplash")
UNSPLASH_ACCESS_KEY = get_optional("UNSPLASH_ACCESS_KEY", "")

NICHE = get_optional("NICHE", "cybersecurity")
POSTING_TIMES = get_optional("POSTING_TIMES", "07:00,09:00,12:00,15:00,18:00,21:00")

MAX_RETRIES = get_int("MAX_RETRIES", 3)
RETRY_DELAY = get_int("RETRY_DELAY", 60)

LOG_LEVEL = get_optional("LOG_LEVEL", "INFO")

USE_AI_IMAGES = get_bool("USE_AI_IMAGES", False)

AI_IMAGE_MODELS = {
    "flux": "flux (default, high quality)",
    "turbo": "turbo (faster generation)",
}

API_VERSION = "v18.0"
GRAPH_API_URL = f"https://graph.facebook.com/{API_VERSION}"

POSTING_HOURS = [7, 9, 12, 15, 18, 21]
