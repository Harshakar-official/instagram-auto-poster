import requests
import logging
import random
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
import config

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.source = config.IMAGE_SOURCE
        self.niche = config.NICHE

    def generate_image(self, prompt=None):
        if self.source == "stable_diffusion":
            return self._generate_with_stable_diffusion(prompt)
        else:
            return self._fetch_from_unsplash()

    def _fetch_from_unsplash(self):
        try:
            search_terms = self._get_search_terms()
            url = "https://api.unsplash.com/photos/random"
            params = {
                "query": search_terms,
                "orientation": "square",
                "content_filter": "high",
            }
            headers = {"Authorization": f"Client-ID {config.UNSPLASH_ACCESS_KEY}"}

            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            image_url = data["urls"]["regular"]

            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            image = Image.open(BytesIO(img_response.content))
            image = image.convert("RGB")

            image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            os.makedirs("images", exist_ok=True)
            image.save(image_path, "JPEG", quality=95)

            logger.info(f"Downloaded image from Unsplash: {data['id']}")
            return image_path, data.get("alt_description", "")

        except Exception as e:
            logger.error(f"Unsplash error: {e}")
            return self._generate_fallback_image()

    def _generate_with_stable_diffusion(self, prompt=None):
        try:
            if not prompt:
                prompt = self._get_ai_prompt()

            api_url = (
                config.STABLE_DIFFUSION_API_URL
                or "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            )

            headers = {
                "Authorization": f"Bearer {config.STABLE_DIFFUSION_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "text_prompts": [{"text": prompt, "weight": 1}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "steps": 30,
                "samples": 1,
            }

            response = requests.post(
                api_url, json=payload, headers=headers, timeout=120
            )
            response.raise_for_status()

            data = response.json()
            image_base64 = data["artifacts"][0]["base64"]

            from base64 import b64decode

            image_data = b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            image = image.convert("RGB")

            os.makedirs("images", exist_ok=True)
            image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            image.save(image_path, "JPEG", quality=95)

            logger.info(f"Generated image with Stable Diffusion")
            return image_path, prompt

        except Exception as e:
            logger.error(f"Stable Diffusion error: {e}")
            return self._generate_fallback_image()

    def _generate_fallback_image(self):
        from PIL import ImageDraw, ImageFont

        img = Image.new("RGB", (1080, 1080), color=(10, 20, 40))
        draw = ImageDraw.Draw(img)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            brightness = random.randint(50, 255)
            draw.ellipse([x, y, x + size, y + size], fill=(0, brightness, brightness))

        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60
            )
            font_small = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30
            )
        except:
            font = None
            font_small = None

        if font:
            draw.text(
                (540, 480), "VAPTANIX", fill=(0, 255, 255), font=font, anchor="mm"
            )
        if font_small:
            draw.text(
                (540, 540),
                "Security Solutions",
                fill=(100, 200, 200),
                font=font_small,
                anchor="mm",
            )

        os.makedirs("images", exist_ok=True)
        image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(image_path, "JPEG", quality=95)

        logger.warning("Using fallback cybersecurity-themed image")
        return image_path, "Generated cybersecurity fallback image"

    def _get_search_terms(self):
        niche_terms = {
            "cybersecurity": "cybersecurity, hacker, technology security, digital protection, network security",
            "tech": "cybersecurity, hacker, technology security, digital protection, network security",
        }
        return niche_terms.get(self.niche, "cybersecurity technology security")

    def _get_ai_prompt(self):
        niche_prompts = {
            "cybersecurity": "Futuristic cybersecurity visualization, digital protection, blue neon lights, secure network, technology, professional",
            "tech": "Futuristic cybersecurity visualization, digital protection, blue neon lights, secure network, technology, professional",
        }
        base_prompt = niche_prompts.get(
            self.niche,
            "Cybersecurity visualization, digital protection, blue neon lights, professional",
        )
        return f"{base_prompt}, Instagram square format, no text, no watermark"
