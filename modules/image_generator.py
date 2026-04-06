import requests
import logging
import random
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.source = config.IMAGE_SOURCE
        self.niche = config.NICHE

    def generate_image(self, prompt=None):
        return self._generate_professional_image()

    def _generate_professional_image(self):
        try:
            os.makedirs("images", exist_ok=True)
            image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            img = self._create_cybersecurity_image()
            img.save(image_path, "JPEG", quality=95)

            logger.info(f"Generated professional cybersecurity image")
            return image_path, "Vaptanix Security Solutions"

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_simple_fallback()

    def _create_cybersecurity_image(self):
        templates = [
            self._create_abstract_tech,
            self._create_lock_security,
            self._create_network_grid,
            self._create_code_matrix,
            self._create_shield_protection,
        ]
        return random.choice(templates)()

    def _create_abstract_tech(self):
        img = Image.new("RGB", (1080, 1080), color=(10, 15, 30))
        draw = ImageDraw.Draw(img)

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 4)
            brightness = random.randint(0, 150)
            draw.ellipse([x, y, x + size, y + size], fill=(0, brightness, brightness))

        for _ in range(20):
            x1, y1 = random.randint(0, 1080), random.randint(0, 1080)
            x2, y2 = random.randint(0, 1080), random.randint(0, 1080)
            draw.line([x1, y1, x2, y2], fill=(0, 100, 150), width=1)

        self._add_branding(draw, 540, 950)
        return img

    def _create_lock_security(self):
        img = Image.new("RGB", (1080, 1080), color=(20, 25, 50))
        draw = ImageDraw.Draw(img)

        for i in range(50):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 3)
            draw.ellipse([x, y, x + size, y + size], fill=(50, 100, 150, 100))

        lock_x, lock_y = 540, 450
        draw.ellipse(
            [lock_x - 100, lock_y - 150, lock_x + 100, lock_y + 50],
            outline=(0, 200, 255),
            width=8,
        )
        draw.rectangle(
            [lock_x - 70, lock_y, lock_x + 70, lock_y + 120],
            fill=(0, 150, 200),
            outline=(0, 200, 255),
            width=4,
        )
        draw.ellipse(
            [lock_x - 15, lock_y + 40, lock_x + 15, lock_y + 70], fill=(10, 15, 30)
        )

        for _ in range(15):
            x = random.randint(100, 980)
            draw.line([x, 0, x, 1080], fill=(0, 50, 100), width=1)
        for _ in range(15):
            y = random.randint(100, 980)
            draw.line([0, y, 1080, y], fill=(0, 50, 100), width=1)

        self._add_branding(draw, 540, 950)
        return img

    def _create_network_grid(self):
        img = Image.new("RGB", (1080, 1080), color=(5, 10, 20))
        draw = ImageDraw.Draw(img)

        nodes = [
            (random.randint(50, 1030), random.randint(50, 1030)) for _ in range(30)
        ]

        for i, (x1, y1) in enumerate(nodes):
            for x2, y2 in nodes[i + 1 : i + 4]:
                dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if dist < 300:
                    draw.line([x1, y1, x2, y2], fill=(0, 100, 150), width=2)

        for x, y in nodes:
            size = random.randint(5, 15)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=(0, 150, 255))

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            draw.point((x, y), fill=(100, 200, 255))

        self._add_branding(draw, 540, 950)
        return img

    def _create_code_matrix(self):
        img = Image.new("RGB", (1080, 1080), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"

        for col in range(0, 1080, 30):
            chars_in_col = [
                chars[random.randint(0, len(chars) - 1)]
                for _ in range(random.randint(20, 50))
            ]
            y = random.randint(-200, 0)
            for char in chars_in_col:
                brightness = random.randint(100, 255)
                color = (
                    (0, brightness, 0)
                    if random.random() > 0.1
                    else (0, brightness // 2, brightness)
                )
                try:
                    draw.text((col, y), char, fill=color)
                except:
                    pass
                y += 25

        for _ in range(50):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            draw.ellipse([x, y, x + 2, y + 2], fill=(0, 255, 0))

        self._add_branding(draw, 540, 1000)
        return img

    def _create_shield_protection(self):
        img = Image.new("RGB", (1080, 1080), color=(10, 15, 35))
        draw = ImageDraw.Draw(img)

        for _ in range(150):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 3)
            draw.ellipse([x, y, x + size, y + size], fill=(50, 100, 150))

        center_x, center_y = 540, 450

        points = [
            (center_x, center_y - 200),
            (center_x + 150, center_y - 100),
            (center_x + 150, center_y + 50),
            (center_x, center_y + 200),
            (center_x - 150, center_y + 50),
            (center_x - 150, center_y - 100),
        ]
        draw.polygon(points, fill=(0, 100, 150), outline=(0, 200, 255))

        inner_points = [
            (center_x, center_y - 150),
            (center_x + 110, center_y - 70),
            (center_x + 110, center_y + 40),
            (center_x, center_y + 150),
            (center_x - 110, center_y + 40),
            (center_x - 110, center_y - 70),
        ]
        draw.polygon(inner_points, fill=(10, 15, 35), outline=(0, 180, 230))

        check_x, check_y = center_x - 30, center_y - 30
        draw.line(
            [check_x, check_y + 50, check_x - 30, check_y + 20],
            fill=(0, 255, 100),
            width=8,
        )
        draw.line(
            [check_x - 30, check_y + 20, check_x + 50, check_y - 40],
            fill=(0, 255, 100),
            width=8,
        )

        for _ in range(8):
            angle = random.uniform(0, 6.28)
            dist = random.randint(200, 450)
            x = center_x + int(dist * 0.7 * (1 if random.random() > 0.5 else -1))
            y = center_y + int(dist * 0.7 * (1 if random.random() > 0.5 else -1))
            size = random.randint(2, 6)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=(100, 200, 255))

        self._add_branding(draw, 540, 950)
        return img

    def _add_branding(self, draw, x, y):
        try:
            draw.text((x, y - 25), "VAPTANIX", fill=(0, 200, 255), anchor="mm")
            draw.text(
                (x, y + 15), "www.vaptanix.com", fill=(100, 180, 200), anchor="mm"
            )
        except:
            pass

    def _create_simple_fallback(self):
        img = Image.new("RGB", (1080, 1080), color=(10, 20, 40))
        draw = ImageDraw.Draw(img)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=(0, 100, 150))

        try:
            draw.text((540, 500), "VAPTANIX", fill=(0, 200, 255), anchor="mm")
            draw.text(
                (540, 560), "Security Solutions", fill=(100, 150, 200), anchor="mm"
            )
            draw.text((540, 620), "www.vaptanix.com", fill=(80, 130, 180), anchor="mm")
        except:
            pass

        os.makedirs("images", exist_ok=True)
        image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(image_path, "JPEG", quality=95)

        logger.warning("Using fallback cybersecurity image")
        return image_path, "Vaptanix Security"

    def _fetch_from_pexels(self):
        try:
            search_terms = self._get_search_terms()
            url = "https://api.pexels.com/v1/search"
            params = {
                "query": search_terms,
                "per_page": 15,
                "orientation": "square",
            }
            headers = {"Authorization": config.PEXELS_API_KEY}

            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            if data["photos"]:
                photo = random.choice(data["photos"])
                img_response = requests.get(photo["src"]["large"], timeout=30)
                img_response.raise_for_status()

                image = Image.open(BytesIO(img_response.content))
                image = image.convert("RGB")
                image = image.resize((1080, 1080), Image.Resampling.LANCZOS)

                image_path = (
                    f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                )
                os.makedirs("images", exist_ok=True)
                image.save(image_path, "JPEG", quality=95)

                logger.info(f"Downloaded image from Pexels: {photo['id']}")
                return image_path, photo.get("alt", "")

        except Exception as e:
            logger.error(f"Pexels error: {e}")

        return self._generate_professional_image()

    def _get_search_terms(self):
        return "cybersecurity, technology, security, hacker, network"
