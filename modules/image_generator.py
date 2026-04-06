import requests
import logging
import random
import os
import math
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import config

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.source = config.IMAGE_SOURCE
        self.niche = config.NICHE

        self.title_font_size = 42
        self.text_font_size = 18
        self.emoji_font_size = 32

    def generate_ai_image(self, prompt):
        try:
            os.makedirs("images", exist_ok=True)
            image_path = (
                f"images/ai_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )

            cyber_prompt = f"cybersecurity, {prompt}, dark theme, professional, digital art, no text"

            result = subprocess.run(
                ["node", "ai_image.js", cyber_prompt, image_path],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0 and os.path.exists(image_path):
                logger.info(f"Generated AI image using Pollinations.ai")
                return image_path
            else:
                logger.error(f"AI image generation failed: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error("AI image generation timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating AI image: {e}")
            return None

    def generate_image(self, caption_text=None):
        try:
            os.makedirs("images", exist_ok=True)
            image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            templates = [
                self._create_infographic_style1,
                self._create_infographic_style2,
                self._create_infographic_style3,
                self._create_infographic_style4,
                self._create_infographic_style5,
                self._create_cybersecurity_dark,
                self._create_cybersecurity_tech,
            ]

            img = random.choice(templates)(caption_text)
            img.save(image_path, "JPEG", quality=95)

            logger.info(f"Generated professional cybersecurity infographic")
            return image_path, "Vaptanix Security"

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_simple_fallback()

    def _create_gradient(self, width, height, color1, color2, direction="vertical"):
        img = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(img)

        for i in range(height if direction == "vertical" else width):
            if direction == "vertical":
                ratio = i / height
            else:
                ratio = i / width

            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

            if direction == "vertical":
                draw.line([(0, i), (width, i)], fill=(r, g, b))
            else:
                draw.line([(i, 0), (i, height)], fill=(r, g, b))

        return img, draw

    def _create_infographic_style1(self, caption=None):
        img, draw = self._create_gradient(1080, 1080, (10, 20, 40), (20, 40, 80))

        draw.rectangle([30, 30, 1050, 1050], outline=(0, 180, 255), width=4)

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 3)
            brightness = random.randint(50, 200)
            draw.ellipse(
                [x, y, x + size, y + size], fill=(0, brightness // 2, brightness)
            )

        self._add_header(draw, "CYBERSECURITY", (0, 200, 255))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_infographic_style2(self, caption=None):
        img = Image.new("RGB", (1080, 1080), (15, 25, 50))
        draw = ImageDraw.Draw(img)

        draw.rectangle([20, 20, 1060, 1060], outline=(0, 220, 200), width=3)
        draw.rectangle([40, 40, 1040, 1040], outline=(0, 180, 150), width=2)

        for _ in range(150):
            x, y = random.randint(50, 1030), random.randint(50, 1030)
            size = random.randint(2, 4)
            brightness = random.randint(50, 150)
            draw.ellipse(
                [x, y, x + size, y + size],
                fill=(brightness // 3, brightness // 2, brightness),
            )

        center_x, center_y = 540, 350

        shield_points = [
            (center_x, center_y - 200),
            (center_x + 180, center_y - 100),
            (center_x + 180, center_y + 50),
            (center_x, center_y + 220),
            (center_x - 180, center_y + 50),
            (center_x - 180, center_y - 100),
        ]
        draw.polygon(shield_points, fill=(0, 100, 180), outline=(0, 200, 255), width=4)

        check_x, check_y = center_x - 40, center_y - 40
        draw.line(
            [check_x, check_y + 80, check_x - 50, check_y + 30],
            fill=(0, 255, 100),
            width=8,
        )
        draw.line(
            [check_x - 50, check_y + 30, check_x + 80, check_y - 60],
            fill=(0, 255, 100),
            width=8,
        )

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_infographic_style3(self, caption=None):
        img = Image.new("RGB", (1080, 1080), (5, 15, 35))
        draw = ImageDraw.Draw(img)

        for i in range(0, 1080, 40):
            draw.line([(i, 0), (i, 1080)], fill=(0, 60, 120), width=1)
            draw.line([(0, i), (1080, i)], fill=(0, 60, 120), width=1)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(3, 6)
            brightness = random.randint(100, 255)
            draw.ellipse(
                [x - size, y - size, x + size, y + size],
                fill=(0, brightness, brightness),
            )

        self._add_header(draw, "SECURITY TIPS", (255, 200, 0))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_infographic_style4(self, caption=None):
        img = Image.new("RGB", (1080, 1080), (20, 10, 40))
        draw = ImageDraw.Draw(img)

        for _ in range(80):
            x = random.randint(0, 1080)
            y = random.randint(0, 1080)
            width = random.randint(20, 80)
            height = random.randint(2, 4)
            brightness = random.randint(50, 150)
            draw.rectangle(
                [x, y, x + width, y + height],
                fill=(brightness, brightness // 3, brightness * 2),
            )

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            brightness = random.randint(100, 200)
            draw.ellipse(
                [x, y, x + size, y + size], fill=(brightness, 100, brightness // 2)
            )

        draw.rectangle([50, 80, 1030, 950], outline=(200, 100, 255), width=4)

        self._add_header(draw, "PROTECT YOUR DATA", (200, 150, 255))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_infographic_style5(self, caption=None):
        img, draw = self._create_gradient(1080, 1080, (0, 30, 60), (10, 50, 100))

        for i in range(5):
            offset = i * 15
            draw.rectangle(
                [100 + offset, 100 + offset, 980 - offset, 980 - offset],
                outline=(0, 200 - i * 20, 255 - i * 30),
                width=2,
            )

        for _ in range(120):
            x, y = random.randint(100, 980), random.randint(100, 980)
            size = random.randint(2, 4)
            brightness = random.randint(50, 200)
            draw.ellipse(
                [x, y, x + size, y + size], fill=(0, brightness // 2, brightness)
            )

        self._add_header(draw, "STAY SECURE", (100, 255, 200))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_cybersecurity_dark(self, caption=None):
        img = Image.new("RGB", (1080, 1080), (10, 10, 15))
        draw = ImageDraw.Draw(img)

        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"

        for col in range(0, 1080, 20):
            chars_in_col = [chars[random.randint(0, len(chars) - 1)] for _ in range(50)]
            y = random.randint(-300, 0)
            for i, char in enumerate(chars_in_col):
                brightness = 255 - (i * 5)
                if brightness > 0:
                    if i < 3:
                        color = (200, 255, 200)
                    else:
                        color = (0, brightness, 0)
                    try:
                        draw.text((col, y), char, fill=color)
                    except:
                        pass
                y += 22

        for _ in range(80):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            draw.ellipse([x, y, x + 2, y + 2], fill=(0, 255, 100))

        self._add_header(draw, "MATRIX SECURITY", (0, 255, 100))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _create_cybersecurity_tech(self, caption=None):
        img, draw = self._create_gradient(1080, 1080, (20, 30, 60), (40, 60, 100))

        center_x, center_y = 540, 350

        nodes = [
            (random.randint(100, 980), random.randint(100, 900)) for _ in range(35)
        ]

        for i, (x1, y1) in enumerate(nodes):
            for x2, y2 in nodes[i + 1 : i + 5]:
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < 300:
                    draw.line([x1, y1, x2, y2], fill=(0, 150, 200), width=2)

        for x, y in nodes:
            size = random.randint(8, 18)
            brightness = random.randint(100, 255)
            draw.ellipse(
                [x - size, y - size, x + size, y + size],
                fill=(0, brightness, brightness),
                outline=(0, 255, 255),
            )

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 2)
            draw.ellipse([x, y, x + size, y + size], fill=(100, 200, 255))

        self._add_header(draw, "NETWORK SECURITY", (0, 200, 255))

        if caption:
            self._add_caption_text(draw, caption)

        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        return img

    def _add_header(self, draw, text, color):
        try:
            draw.rectangle([100, 80, 980, 160], fill=(0, 0, 0, 200))
            draw.text((540, 120), text, fill=color)
        except:
            pass

    def _add_footer(self, draw, name, url):
        try:
            draw.rectangle([200, 950, 880, 1020], fill=(0, 0, 0, 200))
            draw.text((540, 965), name, fill=(0, 200, 255))
            draw.text((540, 995), url, fill=(100, 180, 200))
        except:
            pass

    def _add_caption_text(self, draw, caption):
        try:
            y_pos = 200

            lines = caption.split("\n")

            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    y_pos += 30
                    continue

                if line.startswith("✓"):
                    color = (0, 255, 100)
                    line = "  " + line
                elif line.replace("n", "").replace(" ", "").replace(".", "").isdigit():
                    color = (255, 200, 100)
                elif line.startswith("#"):
                    color = (100, 150, 255)
                    line = line[:50]
                else:
                    color = (255, 255, 255)

                if i == 0 and any(c.isalpha() for c in line):
                    color = (0, 220, 255)

                if len(line) > 35:
                    words = line.split()
                    line1 = ""
                    line2 = ""
                    for word in words:
                        if len(line1 + " " + word) < 35:
                            line1 += (" " + word).strip()
                        else:
                            line2 += (" " + word).strip()

                    if line1:
                        draw.text((80, y_pos), line1, fill=color)
                        y_pos += 35
                    if line2:
                        draw.text((80, y_pos), line2, fill=color)
                        y_pos += 35
                else:
                    draw.text((80, y_pos), line, fill=color)
                    y_pos += 35

                y_pos += 5

                if y_pos > 900:
                    break

        except Exception as e:
            logger.warning(f"Could not add caption text: {e}")

    def _create_simple_fallback(self):
        img = Image.new("RGB", (1080, 1080), (10, 20, 40))
        draw = ImageDraw.Draw(img)

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            brightness = random.randint(50, 150)
            draw.ellipse([x, y, x + size, y + size], fill=(0, brightness, brightness))

        draw.rectangle([100, 100, 980, 980], outline=(0, 200, 255), width=4)

        self._add_header(draw, "VAPTANIX", (0, 200, 255))
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        os.makedirs("images", exist_ok=True)
        image_path = f"images/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(image_path, "JPEG", quality=95)

        logger.warning("Using fallback image")
        return image_path, "Vaptanix Security"
