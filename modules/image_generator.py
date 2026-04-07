import requests
import logging
import random
import os
import math
import subprocess
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config

logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent.parent.resolve()
BASE_DIR = SCRIPT_DIR


class ImageGenerator:
    def __init__(self):
        self.source = config.IMAGE_SOURCE
        self.niche = config.NICHE
        self.images_dir = BASE_DIR / "images"
        self.images_dir.mkdir(exist_ok=True)

        self.font_sizes = {
            "hero": 72,
            "title": 56,
            "subtitle": 42,
            "body": 36,
            "small": 28,
        }

        self.fonts = {}
        for name, size in self.font_sizes.items():
            try:
                self.fonts[name] = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", size
                )
            except:
                self.fonts[name] = ImageFont.load_default()

    def generate_ai_image(self, prompt):
        try:
            self.images_dir.mkdir(exist_ok=True)
            image_path = str(
                self.images_dir
                / f"ai_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )

            prompts = [
                f"professional cybersecurity infographic, clean modern design, {prompt}, vibrant colors, corporate style, no text, high quality illustration",
                f"digital security concept art, {prompt}, professional flat design, bright colors, modern corporate graphics, no text",
            ]
            cyber_prompt = random.choice(prompts)

            result = subprocess.run(
                ["node", str(BASE_DIR / "ai_image.js"), cyber_prompt, image_path],
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
            self.images_dir.mkdir(exist_ok=True)

            content_type = (
                "promo"
                if any(
                    word in caption_text.lower()
                    for word in [
                        "vaptanix",
                        "services",
                        "protect",
                        "security",
                        "contact",
                        "call",
                        "quote",
                        "offer",
                        "discount",
                        "support",
                        "team",
                        "partner",
                        "trust",
                    ]
                )
                else "edu"
            )

            if content_type == "promo":
                layouts = [
                    self._create_promo_ad,
                    self._create_service_card,
                    self._create_cta_banner,
                    self._create_service_grid,
                    self._create_testimonial_style,
                ]
            else:
                layouts = [
                    self._create_professional_infographic,
                    self._create_clean_checklist,
                    self._create_modern_card,
                    self._create_bold_header,
                    self._create_stats_style,
                ]

            img = random.choice(layouts)(caption_text)
            image_path = str(
                self.images_dir / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            img.save(image_path, "JPEG", quality=95)

            logger.info(f"Generated professional image")
            return image_path, "Vaptanix Security"

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_fallback(caption_text)

    def _draw_text_centered(
        self, draw, text, y, font_name="title", color=(255, 255, 255), max_width=1000
    ):
        font = self.fonts.get(font_name, self.fonts["title"])
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

        if text_width > max_width:
            words = text.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])

            bbox1 = draw.textbbox((0, 0), line1, font=font)
            w1 = bbox1[2] - bbox1[0]
            draw.text(((1080 - w1) // 2, y), line1, fill=color, font=font)

            bbox2 = draw.textbbox((0, 0), line2, font=font)
            w2 = bbox2[2] - bbox2[0]
            draw.text(
                ((1080 - w2) // 2, y + self.font_sizes[font_name] + 10),
                line2,
                fill=color,
                font=font,
            )
        else:
            draw.text(((1080 - text_width) // 2, y), text, fill=color, font=font)

    def _draw_box(self, draw, x, y, w, h, fill, outline=None, width=3):
        draw.rectangle([x, y, x + w, y + h], fill=fill)
        if outline:
            draw.rectangle([x, y, x + w, y + h], outline=outline, width=width)

    def _create_professional_infographic(self, caption=None):
        colors = [
            {
                "bg": (15, 25, 50),
                "accent": (0, 200, 255),
                "secondary": (100, 180, 255),
                "highlight": (255, 200, 50),
            },
            {
                "bg": (25, 15, 45),
                "accent": (200, 100, 255),
                "secondary": (150, 130, 200),
                "highlight": (255, 180, 100),
            },
            {
                "bg": (15, 45, 35),
                "accent": (50, 255, 150),
                "secondary": (100, 200, 180),
                "highlight": (255, 220, 100),
            },
            {
                "bg": (50, 25, 20),
                "accent": (255, 140, 80),
                "secondary": (255, 180, 130),
                "highlight": (255, 220, 150),
            },
        ]
        c = random.choice(colors)

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            r = int(c["bg"][0] + (c["secondary"][0] - c["bg"][0]) * ratio * 0.15)
            g = int(c["bg"][1] + (c["secondary"][1] - c["bg"][1]) * ratio * 0.15)
            b = int(c["bg"][2] + (c["secondary"][2] - c["bg"][2]) * ratio * 0.15)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))

        for _ in range(80):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=c["accent"][:3])

        self._draw_box(draw, 40, 40, 1000, 1000, None, c["accent"], 4)

        title = "CYBERSECURITY"
        draw.rectangle([40, 40, 1040, 160], fill=(0, 0, 0, 180))
        self._draw_text_centered(draw, title, 65, "hero", c["accent"])

        if caption:
            lines = caption.split("\n")
            y_pos = 220

            for line in lines:
                line = line.strip()
                if not line:
                    y_pos += 30
                    continue

                if line.startswith("✓"):
                    draw.ellipse([80, y_pos + 5, 100, y_pos + 25], fill=(0, 255, 100))
                    draw.text(
                        (115, y_pos),
                        line[1:].strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 55
                elif line.replace(" ", "").replace(".", "").isdigit() or "%" in line:
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=c["highlight"],
                        font=self.fonts["subtitle"],
                    )
                    y_pos += 60
                elif line.startswith("#"):
                    pass
                elif any(c.isalpha() for c in line):
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 50
                else:
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=(200, 200, 200),
                        font=self.fonts["small"],
                    )
                    y_pos += 45

                if y_pos > 850:
                    break

        brand_y = 970
        draw.rectangle([200, brand_y, 880, 1030], fill=(0, 0, 0, 150))
        draw.text(
            (540, brand_y + 15),
            "VAPTANIX SECURITY",
            fill=c["accent"],
            font=self.fonts["subtitle"],
        )
        draw.text(
            (540, brand_y + 60),
            "www.vaptanix.com",
            fill=(150, 180, 200),
            font=self.fonts["small"],
        )

        return img

    def _create_clean_checklist(self, caption=None):
        c = {
            "bg": (20, 30, 60),
            "accent": (0, 220, 200),
            "check": (0, 255, 150),
            "text": (255, 255, 255),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(60):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(3, 8)
            draw.ellipse([x, y, x + size, y + size], fill=(0, 100, 120))

        self._draw_box(draw, 60, 60, 960, 960, None, c["accent"], 5)

        self._draw_box(draw, 60, 60, 960, 140, (0, 0, 0, 100))
        draw.text(
            (540, 90), "SECURITY CHECKLIST", fill=c["accent"], font=self.fonts["title"]
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]

            y_pos = 260
            box_height = 120
            items = []

            for line in lines[:6]:
                if line.startswith("✓"):
                    items.append(("check", line[1:].strip()))
                elif any(c.isalpha() for c in line):
                    items.append(("text", line))

            for i, (item_type, text) in enumerate(items):
                y = y_pos + i * box_height

                self._draw_box(
                    draw, 100, y, 880, box_height - 15, (0, 0, 0, 80), c["accent"], 2
                )

                draw.ellipse([130, y + 30, 170, y + 70], fill=c["check"])
                draw.text(
                    (145, y + 38), "✓", fill=(255, 255, 255), font=self.fonts["small"]
                )

                draw.text(
                    (200, y + 30), text, fill=(255, 255, 255), font=self.fonts["body"]
                )

        draw.rectangle([200, 940, 880, 1030], fill=(0, 0, 0, 150))
        draw.text((540, 955), "VAPTANIX", fill=c["accent"], font=self.fonts["subtitle"])
        draw.text(
            (540, 995), "vaptanix.com", fill=(150, 180, 200), font=self.fonts["small"]
        )

        return img

    def _create_modern_card(self, caption=None):
        colors = [
            {"bg": (30, 20, 60), "accent": (150, 100, 255), "card": (50, 40, 80)},
            {"bg": (20, 50, 70), "accent": (100, 200, 255), "card": (30, 70, 100)},
            {"bg": (40, 50, 30), "accent": (150, 255, 150), "card": (50, 70, 40)},
        ]
        c = random.choice(colors)

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        draw.ellipse([-200, -200, 500, 500], fill=c["card"])
        draw.ellipse([600, 600, 1280, 1280], fill=c["card"])

        for _ in range(50):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            draw.ellipse([x, y, x + 4, y + 4], fill=(255, 255, 255, 50))

        self._draw_box(draw, 80, 80, 920, 920, c["card"], c["accent"], 4)

        draw.rectangle([80, 80, 1000, 220], fill=(0, 0, 0, 120))

        title = "CYBER TIPS"
        draw.text((540, 105), title, fill=c["accent"], font=self.fonts["hero"])

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]
            y_pos = 280

            for line in lines[:5]:
                if line.startswith("✓"):
                    draw.ellipse([120, y_pos + 8, 155, y_pos + 43], fill=c["accent"])
                    draw.text(
                        (128, y_pos + 12), "✓", fill=(0, 0, 0), font=self.fonts["small"]
                    )
                    draw.text(
                        (180, y_pos + 5),
                        line[1:].strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 80
                elif any(c.isalpha() for c in line):
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 60

        draw.rectangle([200, 940, 880, 1030], fill=(0, 0, 0, 150))
        draw.text((540, 955), "VAPTANIX", fill=c["accent"], font=self.fonts["subtitle"])
        draw.text(
            (540, 1000),
            "www.vaptanix.com",
            fill=(180, 180, 180),
            font=self.fonts["small"],
        )

        return img

    def _create_bold_header(self, caption=None):
        c = {
            "bg": (10, 15, 35),
            "accent": (0, 200, 255),
            "highlight": (255, 180, 50),
            "text": (240, 240, 240),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(0, 1080, 60):
            alpha = 30 if i % 120 == 0 else 15
            draw.line([(i, 0), (i, 1080)], fill=(0, 80, 120, alpha))
        for i in range(0, 1080, 60):
            draw.line([(0, i), (1080, i)], fill=(0, 80, 120, 15))

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 6)
            draw.ellipse([x, y, x + size, y + size], fill=c["accent"])

        draw.rectangle([0, 0, 1080, 280], fill=(0, 0, 0, 200))

        shield = [(540, 50), (620, 90), (620, 180), (540, 250), (460, 180), (460, 90)]
        draw.polygon(shield, fill=c["bg"], outline=c["accent"], width=4)
        draw.ellipse([510, 110, 570, 170], fill=c["accent"])
        draw.text((528, 125), "✓", fill=c["bg"], font=ImageFont.load_default())

        draw.text((540, 55), "PROTECT", fill=c["accent"], font=self.fonts["hero"])
        draw.text(
            (540, 130), "YOUR BUSINESS", fill=c["text"], font=self.fonts["subtitle"]
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]
            y_pos = 340

            for line in lines[:6]:
                if line.startswith("✓"):
                    draw.ellipse([100, y_pos + 5, 140, y_pos + 45], fill=(0, 255, 100))
                    draw.text(
                        (150, y_pos),
                        line[1:].strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 70
                elif any(c.isalpha() for c in line) and len(line) < 40:
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=c["highlight"],
                        font=self.fonts["subtitle"],
                    )
                    y_pos += 70

        draw.rectangle([100, 920, 980, 1030], fill=(0, 0, 0, 150))
        draw.text(
            (540, 940),
            "VAPTANIX SECURITY",
            fill=c["accent"],
            font=self.fonts["subtitle"],
        )
        draw.text(
            (540, 985), "vaptanix.com", fill=(150, 180, 200), font=self.fonts["small"]
        )

        return img

    def _create_stats_style(self, caption=None):
        c = {
            "bg": (25, 35, 65),
            "accent": (100, 180, 255),
            "highlight": (255, 200, 80),
            "success": (100, 255, 150),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            r = int(c["bg"][0] + 20 * ratio)
            g = int(c["bg"][1] + 15 * ratio)
            b = int(c["bg"][2] + 25 * ratio)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))

        draw.rectangle([40, 40, 1040, 1040], outline=c["accent"], width=5)

        draw.rectangle([40, 40, 1040, 180], fill=(0, 0, 0, 180))
        draw.text((540, 70), "CYBERSECURITY", fill=c["accent"], font=self.fonts["hero"])
        draw.text(
            (540, 140),
            "ESSENTIAL TIPS",
            fill=(200, 200, 200),
            font=self.fonts["subtitle"],
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]

            y_pos = 240
            col = 0
            row = 0
            box_w = 480
            box_h = 150
            margin = 40

            items = []
            for line in lines[:6]:
                if line.startswith("✓"):
                    items.append(("tip", line[1:].strip()))
                elif any(c.isalpha() for c in line):
                    items.append(("info", line))

            for i, (item_type, text) in enumerate(items):
                col = i % 2
                row = i // 2

                x = 60 + col * (box_w + margin)
                y = y_pos + row * (box_h + 20)

                color = c["success"] if item_type == "tip" else c["highlight"]

                self._draw_box(draw, x, y, box_w, box_h, (0, 0, 0, 100), color, 3)

                draw.ellipse([x + 20, y + 20, x + 60, y + 60], fill=color)
                draw.text(
                    (x + 30, y + 25),
                    str(i + 1),
                    fill=(0, 0, 0),
                    font=self.fonts["small"],
                )

                words = text.split()
                if len(words) > 4:
                    mid = len(words) // 2
                    line1 = " ".join(words[:mid])
                    line2 = " ".join(words[mid:])
                    draw.text(
                        (x + 80, y + 30),
                        line1,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    draw.text(
                        (x + 80, y + 70),
                        line2,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                else:
                    draw.text(
                        (x + 80, y + 45),
                        text,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )

        draw.rectangle([200, 940, 880, 1030], fill=(0, 0, 0, 150))
        draw.text((540, 955), "VAPTANIX", fill=c["accent"], font=self.fonts["subtitle"])
        draw.text(
            (540, 1000),
            "vaptanix.com | vaptanixsecurity",
            fill=(150, 180, 200),
            font=self.fonts["small"],
        )

        return img

    def _create_promo_ad(self, caption=None):
        c = {
            "bg": (15, 25, 50),
            "accent": (255, 200, 50),
            "cta": (0, 255, 150),
            "text": (255, 255, 255),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            r = int(c["bg"][0] + 30 * ratio)
            g = int(c["bg"][1] + 20 * ratio)
            b = int(c["bg"][2] + 15 * ratio)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))

        for _ in range(80):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(3, 8)
            draw.ellipse([x, y, x + size, y + size], fill=(255, 200, 50, 80))

        draw.rectangle([0, 0, 1080, 320], fill=(0, 0, 0, 200))

        shield = [(540, 50), (650, 100), (650, 200), (540, 280), (430, 200), (430, 100)]
        draw.polygon(shield, fill=(0, 0, 0, 0), outline=c["accent"], width=5)
        draw.ellipse([500, 110, 580, 190], fill=c["accent"])
        draw.text((520, 130), "VAPTANIX", fill=c["bg"], font=ImageFont.load_default())

        draw.text((540, 60), "PROFESSIONAL", fill=c["accent"], font=self.fonts["hero"])
        draw.text(
            (540, 140), "SECURITY SERVICES", fill=c["text"], font=self.fonts["subtitle"]
        )
        draw.text(
            (540, 210),
            "protecting businesses nationwide",
            fill=(200, 200, 200),
            font=self.fonts["small"],
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ]
            y_pos = 380

            for line in lines[:8]:
                if any(
                    word in line.upper()
                    for word in [
                        "VAPTANIX",
                        "CONTACT",
                        "CALL",
                        "QUOTE",
                        "OFFER",
                        "HURRY",
                        "TODAY",
                        "NOW",
                        "GET",
                        "TRY",
                    ]
                ):
                    draw.rectangle(
                        [100, y_pos - 5, 980, y_pos + 50], fill=(255, 200, 50, 50)
                    )
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=c["accent"],
                        font=self.fonts["subtitle"],
                    )
                    y_pos += 65
                elif line.startswith("✓") or "→" in line:
                    symbol = "✓" if "✓" in line else "→"
                    draw.text(
                        (150, y_pos), symbol, fill=c["cta"], font=self.fonts["body"]
                    )
                    draw.text(
                        (190, y_pos),
                        line.replace("✓", "").replace("→", "").strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 55
                elif len(line) < 50 and any(c.isalpha() for c in line):
                    draw.text(
                        (540, y_pos),
                        line,
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 55

        draw.rectangle([50, 920, 1030, 1030], fill=c["accent"])
        draw.text(
            (540, 935), "CONTACT US TODAY!", fill=c["bg"], font=self.fonts["title"]
        )
        draw.text(
            (540, 990),
            "www.vaptanix.com | Get Protected Now",
            fill=(50, 50, 50),
            font=self.fonts["small"],
        )

        return img

    def _create_service_card(self, caption=None):
        c = {
            "bg": (25, 20, 50),
            "accent": (150, 100, 255),
            "card": (40, 30, 70),
            "cta": (0, 255, 200),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        draw.ellipse([-300, -300, 400, 400], fill=(80, 60, 120))
        draw.ellipse([700, 700, 1400, 1400], fill=(80, 60, 120))

        for _ in range(60):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            draw.ellipse([x, y, x + 3, y + 3], fill=(200, 200, 255, 50))

        self._draw_box(draw, 60, 60, 960, 960, c["card"], c["accent"], 5)

        draw.rectangle([60, 60, 1020, 200], fill=(0, 0, 0, 150))
        draw.text((540, 75), "OUR SERVICES", fill=c["accent"], font=self.fonts["hero"])
        draw.text(
            (540, 145),
            "Comprehensive Security Solutions",
            fill=(200, 200, 200),
            font=self.fonts["body"],
        )

        services = [
            ("PENETRATION TESTING", "Network & Web App"),
            ("VULNERABILITY SCAN", "Automated & Manual"),
            ("SECURITY AUDIT", "Compliance Ready"),
            ("INCIDENT RESPONSE", "24/7 Support"),
        ]

        y_pos = 260
        for i, (service, desc) in enumerate(services):
            y = y_pos + i * 150

            self._draw_box(draw, 100, y, 880, 130, (0, 0, 0, 80), c["accent"], 2)

            draw.ellipse([120, y + 25, 180, y + 85], fill=c["accent"])
            draw.text((135, y + 35), str(i + 1), fill=c["bg"], font=self.fonts["body"])

            draw.text(
                (200, y + 20),
                service,
                fill=(255, 255, 255),
                font=self.fonts["subtitle"],
            )
            draw.text(
                (200, y + 70), desc, fill=(180, 180, 180), font=self.fonts["small"]
            )

            draw.text((850, y + 35), "→", fill=c["cta"], font=self.fonts["title"])

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ][:3]
            y_pos = 880
            for line in lines:
                if any(
                    word in line.upper()
                    for word in ["CONTACT", "CALL", "QUOTE", "VISIT"]
                ):
                    draw.text(
                        (540, y_pos), line, fill=c["cta"], font=self.fonts["body"]
                    )
                    y_pos += 40

        draw.rectangle([200, 950, 880, 1030], fill=(0, 0, 0, 150))
        draw.text((540, 960), "VAPTANIX", fill=c["accent"], font=self.fonts["subtitle"])
        draw.text(
            (540, 1000),
            "vaptanix.com | info@vaptanix.com",
            fill=(180, 180, 180),
            font=self.fonts["small"],
        )

        return img

    def _create_cta_banner(self, caption=None):
        c = {
            "bg": (20, 10, 40),
            "accent": (255, 100, 200),
            "highlight": (255, 220, 50),
            "cta": (0, 255, 150),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(0, 1080, 30):
            alpha = 40 if i % 60 == 0 else 20
            draw.line([(i, 0), (i, 1080)], fill=(100, 50, 150, alpha))

        for _ in range(150):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 6)
            draw.ellipse([x, y, x + size, y + size], fill=(255, 100, 200, 80))

        draw.rectangle([0, 0, 1080, 350], fill=(0, 0, 0, 200))

        draw.text(
            (540, 50), "NEED SECURITY?", fill=c["highlight"], font=self.fonts["hero"]
        )
        draw.text(
            (540, 140),
            "GET PROFESSIONAL HELP NOW",
            fill=(255, 255, 255),
            font=self.fonts["title"],
        )
        draw.text(
            (540, 220),
            "Don't wait for a breach",
            fill=(200, 200, 200),
            font=self.fonts["body"],
        )
        draw.text(
            (540, 270),
            "Protect your business today",
            fill=(200, 200, 200),
            font=self.fonts["body"],
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ]
            y_pos = 400

            for line in lines[:6]:
                if any(
                    word in line.upper()
                    for word in [
                        "CONTACT",
                        "CALL",
                        "QUOTE",
                        "OFFER",
                        "HURRY",
                        "TODAY",
                        "NOW",
                        "GET STARTED",
                        "DM",
                    ]
                ):
                    draw.rectangle(
                        [100, y_pos - 5, 980, y_pos + 55], fill=c["highlight"]
                    )
                    draw.text(
                        (540, y_pos), line, fill=(0, 0, 0), font=self.fonts["subtitle"]
                    )
                    y_pos += 75
                elif line.startswith("✓") or "→" in line:
                    symbol = "✓" if "✓" in line else "→"
                    color = c["cta"] if "✓" in line else c["accent"]
                    draw.text((200, y_pos), symbol, fill=color, font=self.fonts["body"])
                    draw.text(
                        (240, y_pos),
                        line.replace("✓", "").replace("→", "").strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 55

        draw.rectangle([50, 880, 1030, 1030], fill=c["cta"])
        draw.text(
            (540, 895), "CONTACT VAPTANIX NOW!", fill=(0, 0, 0), font=self.fonts["hero"]
        )
        draw.text(
            (540, 970),
            "vaptanix.com | Your Trusted Security Partner",
            fill=(50, 80, 50),
            font=self.fonts["body"],
        )

        return img

    def _create_service_grid(self, caption=None):
        c = {
            "bg": (30, 35, 50),
            "accent": (100, 200, 255),
            "highlight": (255, 180, 100),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            r = int(c["bg"][0] + 15 * ratio)
            g = int(c["bg"][1] + 10 * ratio)
            b = int(c["bg"][2] + 20 * ratio)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))

        draw.rectangle([30, 30, 1050, 1050], outline=c["accent"], width=5)

        draw.rectangle([30, 30, 1050, 150], fill=(0, 0, 0, 180))
        draw.text(
            (540, 50), "VAPTANIX SERVICES", fill=c["accent"], font=self.fonts["hero"]
        )
        draw.text(
            (540, 115),
            "Complete Cybersecurity Solutions",
            fill=(200, 200, 200),
            font=self.fonts["body"],
        )

        services = [
            ("WEB SECURITY", "Web App Testing", c["accent"]),
            ("NETWORK SECURITY", "Penetration Testing", c["highlight"]),
            ("CLOUD SECURITY", "AWS, Azure, GCP", c["accent"]),
            ("MOBILE SECURITY", "iOS & Android", c["highlight"]),
            ("API SECURITY", "REST & GraphQL", c["accent"]),
            ("SOCIAL ENGINEERING", "Human Testing", c["highlight"]),
        ]

        y_pos = 200
        for i, (title, desc, color) in enumerate(services):
            row = i // 2
            col = i % 2

            x = 60 + col * 500
            y = y_pos + row * 200

            self._draw_box(draw, x, y, 460, 170, (0, 0, 0, 80), color, 3)

            draw.ellipse([x + 20, y + 20, x + 70, y + 70], fill=color)
            draw.text(
                (x + 32, y + 28), str(i + 1), fill=(0, 0, 0), font=self.fonts["small"]
            )

            draw.text(
                (x + 90, y + 25),
                title,
                fill=(255, 255, 255),
                font=self.fonts["subtitle"],
            )
            draw.text(
                (x + 90, y + 70), desc, fill=(180, 180, 180), font=self.fonts["small"]
            )

            draw.text((x + 350, y + 100), "→", fill=color, font=self.fonts["title"])

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ][:2]
            y_pos = 870
            for line in lines:
                if any(
                    word in line.upper()
                    for word in ["CONTACT", "CALL", "QUOTE", "VISIT", "DM", "HURRY"]
                ):
                    draw.text(
                        (540, y_pos), line, fill=c["highlight"], font=self.fonts["body"]
                    )
                    y_pos += 40

        draw.rectangle([200, 940, 880, 1030], fill=(0, 0, 0, 150))
        draw.text(
            (540, 955),
            "www.vaptanix.com",
            fill=c["accent"],
            font=self.fonts["subtitle"],
        )
        draw.text(
            (540, 1000),
            "Get a Free Quote Today!",
            fill=(200, 200, 200),
            font=self.fonts["body"],
        )

        return img

    def _create_testimonial_style(self, caption=None):
        c = {
            "bg": (15, 30, 50),
            "accent": (255, 200, 80),
            "star": (255, 220, 50),
            "quote": (200, 220, 255),
            "cta": (0, 255, 150),
        }

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=(255, 200, 80, 50))

        self._draw_box(draw, 50, 50, 980, 980, None, c["accent"], 5)

        draw.rectangle([50, 50, 1030, 200], fill=(0, 0, 0, 180))
        draw.text((540, 65), "WHY VAPTANIX?", fill=c["accent"], font=self.fonts["hero"])

        for i in range(5):
            x = 250 + i * 130
            draw.text((x, 130), "★", fill=c["star"], font=ImageFont.load_default())
        draw.text(
            (540, 165),
            "Trusted by 500+ Businesses",
            fill=(200, 200, 200),
            font=self.fonts["small"],
        )

        stats = [
            ("500+", "Projects Done"),
            ("1000+", "Vulns Found"),
            ("99%", "Satisfaction"),
            ("24/7", "Support"),
        ]

        y_pos = 250
        box_w = 230
        for i, (num, label) in enumerate(stats):
            x = 80 + i * (box_w + 20)

            self._draw_box(draw, x, y_pos, box_w, 150, (0, 0, 0, 100), c["accent"], 3)

            draw.text(
                (x + box_w // 2, y_pos + 20),
                num,
                fill=c["star"],
                font=self.fonts["hero"],
            )
            draw.text(
                (x + box_w // 2, y_pos + 90),
                label,
                fill=(200, 200, 200),
                font=self.fonts["body"],
            )

        why_us = [
            "Certified Ethical Hackers",
            "Latest Tools & Techniques",
            "Comprehensive Reports",
            "Affordable Pricing",
            "Excellent Support",
        ]

        y_pos = 450
        draw.rectangle([80, y_pos, 1000, y_pos + 320], fill=(0, 0, 0, 100))

        draw.text(
            (540, y_pos + 10),
            "WHY CHOOSE US?",
            fill=c["accent"],
            font=self.fonts["subtitle"],
        )

        y_pos += 60
        for i, item in enumerate(why_us):
            col = i % 2
            row = i // 2

            x = 120 + col * 460
            y = y_pos + row * 70

            draw.ellipse([x, y + 5, x + 30, y + 35], fill=c["cta"])
            draw.text(
                (x + 5, y + 8), "✓", fill=(0, 0, 0), font=ImageFont.load_default()
            )
            draw.text(
                (x + 45, y + 5), item, fill=(255, 255, 255), font=self.fonts["body"]
            )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ][:3]
            y_pos = 800
            for line in lines:
                if any(
                    word in line.upper()
                    for word in ["CONTACT", "CALL", "QUOTE", "PARTNER"]
                ):
                    draw.text(
                        (540, y_pos), line, fill=c["quote"], font=self.fonts["body"]
                    )
                    y_pos += 40

        draw.rectangle([150, 930, 930, 1030], fill=(0, 0, 0, 150))
        draw.text((540, 945), "VAPTANIX", fill=c["accent"], font=self.fonts["subtitle"])
        draw.text(
            (540, 990),
            "Your Trusted Security Partner | vaptanix.com",
            fill=(180, 180, 180),
            font=self.fonts["small"],
        )

        return img

    def _create_fallback(self, caption=None):
        c = {"bg": (20, 30, 60), "accent": (0, 200, 255)}

        img = Image.new("RGB", (1080, 1080), c["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=c["accent"])

        self._draw_box(draw, 60, 60, 960, 960, None, c["accent"], 5)

        draw.rectangle([60, 60, 1020, 180], fill=(0, 0, 0, 150))
        draw.text(
            (540, 85), "VAPTANIX SECURITY", fill=c["accent"], font=self.fonts["title"]
        )

        if caption:
            lines = [
                l.strip()
                for l in caption.split("\n")
                if l.strip() and not l.startswith("#")
            ][:6]
            y_pos = 250
            for line in lines:
                if line.startswith("✓"):
                    draw.ellipse([100, y_pos + 5, 140, y_pos + 45], fill=(0, 255, 100))
                    draw.text(
                        (150, y_pos),
                        line[1:].strip(),
                        fill=(255, 255, 255),
                        font=self.fonts["body"],
                    )
                    y_pos += 70

        image_path = str(
            self.images_dir / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        img.save(image_path, "JPEG", quality=95)
        return image_path, "Vaptanix Security"
