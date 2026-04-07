import requests
import logging
import random
import os
import math
import subprocess
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
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

        try:
            self.font_large = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc", 65
            )
            self.font_medium = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc", 42
            )
            self.font_small = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc", 32
            )
            self.font_tiny = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc", 26
            )
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

        self.COLOR_PALETTES = [
            {
                "bg": (25, 55, 95),
                "accent": (0, 200, 255),
                "secondary": (100, 180, 255),
                "glow": (0, 150, 255),
            },
            {
                "bg": (45, 20, 80),
                "accent": (255, 100, 200),
                "secondary": (200, 150, 255),
                "glow": (180, 80, 220),
            },
            {
                "bg": (20, 60, 40),
                "accent": (0, 255, 150),
                "secondary": (100, 255, 200),
                "glow": (0, 200, 100),
            },
            {
                "bg": (80, 30, 20),
                "accent": (255, 120, 50),
                "secondary": (255, 180, 100),
                "glow": (220, 100, 50),
            },
            {
                "bg": (15, 25, 55),
                "accent": (100, 150, 255),
                "secondary": (150, 200, 255),
                "glow": (80, 120, 220),
            },
            {
                "bg": (50, 35, 20),
                "accent": (255, 200, 100),
                "secondary": (255, 220, 150),
                "glow": (230, 180, 80),
            },
            {
                "bg": (30, 50, 50),
                "accent": (100, 255, 255),
                "secondary": (150, 255, 255),
                "glow": (80, 220, 220),
            },
            {
                "bg": (60, 20, 60),
                "accent": (255, 150, 255),
                "secondary": (200, 180, 255),
                "glow": (200, 100, 220),
            },
            {
                "bg": (20, 45, 70),
                "accent": (0, 220, 200),
                "secondary": (100, 240, 220),
                "glow": (0, 180, 160),
            },
            {
                "bg": (70, 45, 25),
                "accent": (255, 180, 80),
                "secondary": (255, 210, 130),
                "glow": (240, 160, 60),
            },
            {
                "bg": (40, 40, 40),
                "accent": (200, 200, 200),
                "secondary": (180, 180, 180),
                "glow": (150, 150, 150),
            },
            {
                "bg": (25, 45, 80),
                "accent": (150, 200, 255),
                "secondary": (200, 220, 255),
                "glow": (120, 170, 230),
            },
        ]

        self.HEADER_TITLES = [
            "VAPTANIX",
            "CYBER SECURE",
            "VAPT",
            "SECURITY",
            "PROTECT",
            "DEFEND",
            "SECURE",
            "GUARD",
            "VAPTANIX",
            "CYBER",
            "NETSEC",
            "INFOSEC",
            "HACK PROOF",
            "ZERO DAY",
            "PATCH NOW",
            "STAY SAFE",
        ]

    def generate_ai_image(self, prompt):
        try:
            self.images_dir.mkdir(exist_ok=True)
            image_path = str(
                self.images_dir
                / f"ai_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )

            prompts = [
                f"professional cybersecurity illustration, modern flat design, {prompt}, vibrant colors, digital protection concept, no text",
                f"futuristic security technology art, {prompt}, neon accents, clean modern style, cyber defense visualization, no text",
                f"abstract digital security concept, {prompt}, holographic elements, tech aesthetic, professional infographic style, no text",
                f"cyber protection illustration, {prompt}, glowing shield elements, modern design, corporate tech style, no text",
                f"network security artwork, {prompt}, data visualization, futuristic tech, clean minimal style, no text",
                f"digital safety concept art, {prompt}, secure lock elements, modern graphics, professional look, no text",
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
            image_path = str(
                self.images_dir / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )

            templates = [
                self._create_gradient_vibes,
                self._create_geometric_shield,
                self._create_particle_waves,
                self._create_abstract_tech,
                self._create_minimal_circuit,
                self._create_data_stream,
                self._create_modern_layers,
                self._create_neon_rings,
                self._create_hex_pattern,
                self._create_glitch_art,
                self._create_wave_gradient,
                self._create_polygon_mesh,
            ]

            img = random.choice(templates)(caption_text)
            img.save(image_path, "JPEG", quality=95)

            logger.info(f"Generated creative image")
            return image_path, "Vaptanix Security"

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_simple_fallback()

    def _get_palette(self):
        return random.choice(self.COLOR_PALETTES)

    def _create_gradient_vibes(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            r = int(p["bg"][0] * (1 - ratio) + p["secondary"][0] * ratio * 0.3)
            g = int(p["bg"][1] * (1 - ratio) + p["secondary"][1] * ratio * 0.3)
            b = int(p["bg"][2] * (1 - ratio) + p["secondary"][2] * ratio * 0.3)
            draw.line([(0, i), (1080, i)], fill=(r, g, b))

        for _ in range(150):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(3, 8)
            alpha = random.randint(50, 150)
            color = tuple(min(255, c + alpha) for c in p["accent"])
            draw.ellipse([x, y, x + size, y + size], fill=color)

        circles = [
            (random.randint(100, 980), random.randint(100, 980)) for _ in range(5)
        ]
        for cx, cy in circles:
            r = random.randint(80, 200)
            for ring in range(3):
                draw.ellipse(
                    [
                        cx - r + ring * 20,
                        cy - r + ring * 20,
                        cx + r - ring * 20,
                        cy + r - ring * 20,
                    ],
                    outline=p["glow"],
                    width=2,
                )

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_geometric_shield(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        center_x, center_y = 540, 480
        shield = [
            (center_x, center_y - 280),
            (center_x + 220, center_y - 150),
            (center_x + 220, center_y + 50),
            (center_x, center_y + 320),
            (center_x - 220, center_y + 50),
            (center_x - 220, center_y - 150),
        ]
        draw.polygon(shield, fill=p["bg"], outline=p["accent"], width=5)

        inner_shield = (
            [(x + (y - center_y) * 0.15, y) for x, y in shield[:4]]
            + [(center_x, center_y + 150), (center_x, center_y + 100)]
            + [(x + (y - center_y) * 0.15, y) for x, y in shield[4:]]
        )
        draw.polygon(inner_shield[:6], fill=None, outline=p["glow"], width=3)

        for _ in range(50):
            x = center_x + random.randint(-180, 180)
            y = center_y + random.randint(-150, 180)
            size = random.randint(2, 4)
            draw.ellipse([x, y, x + size, y + size], fill=p["secondary"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_particle_waves(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for wave in range(5):
            points = []
            y_base = 200 + wave * 180
            for x in range(0, 1081, 20):
                y = y_base + math.sin(x * 0.01 + wave) * 50
                points.append((x, y))
            points.append((1080, 1080))
            points.append((0, 1080))

            color = tuple(max(0, min(255, c + wave * 20)) for c in p["accent"])
            draw.polygon(points, fill=(*color, 30))

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 4)
            brightness = random.randint(100, 255)
            color = tuple(min(255, c + brightness // 3) for c in p["accent"])
            draw.ellipse([x, y, x + size, y + size], fill=color)

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_abstract_tech(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        shapes = []
        for _ in range(8):
            shape_type = random.choice(["rect", "ellipse", "polygon"])
            x, y = random.randint(100, 800), random.randint(100, 800)
            size = random.randint(100, 300)

            if shape_type == "rect":
                angle = random.randint(0, 45)
                points = [
                    (x, y),
                    (x + size, y),
                    (x + size, y + int(size * 0.6)),
                    (x, y + int(size * 0.6)),
                ]
                if angle:
                    cx, cy = x + size // 2, y + size // 3
                    import math

                    angle_rad = math.radians(angle)
                    points = []
                    for px, py in [
                        (x, y),
                        (x + size, y),
                        (x + size, y + int(size * 0.6)),
                        (x, y + int(size * 0.6)),
                    ]:
                        nx = (
                            cx
                            + (px - cx) * math.cos(angle_rad)
                            - (py - cy) * math.sin(angle_rad)
                        )
                        ny = (
                            cy
                            + (px - cx) * math.sin(angle_rad)
                            + (py - cy) * math.cos(angle_rad)
                        )
                        points.append((nx, ny))
                draw.polygon(points, fill=None, outline=p["accent"], width=3)
            elif shape_type == "ellipse":
                draw.ellipse(
                    [x, y, x + size, y + size], fill=None, outline=p["glow"], width=3
                )
            else:
                pts = [
                    (x + random.randint(0, size), y + random.randint(0, size))
                    for _ in range(6)
                ]
                draw.polygon(pts, fill=None, outline=p["secondary"], width=2)

        for _ in range(150):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 4)
            draw.ellipse([x, y, x + size, y + size], fill=p["accent"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_minimal_circuit(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        nodes = [
            (random.randint(50, 1030), random.randint(50, 1030)) for _ in range(40)
        ]

        for i, (x1, y1) in enumerate(nodes):
            for x2, y2 in nodes[i + 1 :]:
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < 200:
                    draw.line([x1, y1, x2, y2], fill=p["glow"], width=2)

        for x, y in nodes:
            size = random.randint(6, 12)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=p["accent"])
            draw.ellipse(
                [x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                fill=p["secondary"],
            )

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 2)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_data_stream(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for col in range(0, 1080, 8):
            for row in range(0, 1080, 12):
                if random.random() > 0.3:
                    brightness = random.randint(50, 255)
                    color = tuple(min(255, c + brightness // 3) for c in p["accent"])
                    height = random.randint(5, 20)
                    draw.rectangle([col, row, col + 4, row + height], fill=color)

        for _ in range(50):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(4, 10)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_modern_layers(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for layer in range(5):
            y_offset = layer * 150
            opacity = 100 - layer * 15

            x_offset = random.randint(-50, 50)

            draw.ellipse(
                [100 + x_offset, 300 + y_offset, 980 + x_offset, 700 + y_offset],
                fill=(*p["accent"], opacity)
                if isinstance(p["accent"], tuple)
                else p["accent"],
            )
            draw.ellipse(
                [150 + x_offset, 350 + y_offset, 930 + x_offset, 650 + y_offset],
                fill=p["bg"],
            )

        for _ in range(120):
            x, y = random.randint(100, 980), random.randint(100, 980)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=p["secondary"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_neon_rings(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        cx, cy = 540, 400
        for ring in range(8):
            radius = 80 + ring * 60
            offset = math.sin(ring) * 20
            draw.ellipse(
                [cx - radius + offset, cy - radius, cx + radius + offset, cy + radius],
                outline=p["glow"],
                width=3,
            )

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 3)
            draw.ellipse([x, y, x + size, y + size], fill=p["accent"])

        for i in range(3):
            start_x = random.randint(200, 880)
            start_y = cy + 250
            draw.line(
                [
                    start_x,
                    start_y,
                    start_x + random.randint(-100, 100),
                    start_y + random.randint(100, 200),
                ],
                fill=p["secondary"],
                width=2,
            )

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_hex_pattern(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        hex_size = 40
        for row in range(-2, 25):
            for col in range(-2, 15):
                x_offset = 0 if row % 2 == 0 else hex_size
                x = col * hex_size * 1.5 + x_offset + 50
                y = row * hex_size * 1.732 + 50

                if random.random() > 0.4:
                    points = []
                    for i in range(6):
                        angle = math.radians(60 * i - 30)
                        points.append(
                            (
                                x + hex_size * math.cos(angle),
                                y + hex_size * math.sin(angle),
                            )
                        )
                    draw.polygon(points, outline=p["glow"], width=1)

        for _ in range(100):
            x, y = random.randint(50, 1030), random.randint(50, 1030)
            size = random.randint(2, 4)
            draw.ellipse([x, y, x + size, y + size], fill=p["accent"])

        cx, cy = 540, 480
        shield = [
            (cx, cy - 150),
            (cx + 100, cy - 80),
            (cx + 100, cy + 30),
            (cx, cy + 130),
            (cx - 100, cy + 30),
            (cx - 100, cy - 80),
        ]
        draw.polygon(shield, fill=p["bg"], outline=p["accent"], width=4)

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_glitch_art(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(30):
            y = random.randint(0, 1080)
            height = random.randint(2, 8)
            offset = random.randint(-30, 30)
            color = tuple(random.randint(0, 255) for _ in range(3))
            draw.rectangle([0, y, 1080, y + height], fill=color)

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            color = tuple(min(255, c + random.randint(0, 50)) for c in p["accent"])
            draw.ellipse([x, y, x + size, y + size], fill=color)

        for _ in range(10):
            x = random.randint(100, 900)
            y = random.randint(100, 900)
            w = random.randint(50, 200)
            draw.rectangle([x, y, x + w, y + 3], fill=p["glow"])
            draw.rectangle([x + offset, y, x + w + offset, y + 3], fill=p["accent"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_wave_gradient(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for i in range(1080):
            ratio = i / 1080
            wave = math.sin(i * 0.005) * 20
            r = int(p["bg"][0] + (p["accent"][0] - p["bg"][0]) * ratio + wave)
            g = int(p["bg"][1] + (p["accent"][1] - p["bg"][1]) * ratio)
            b = int(p["bg"][2] + (p["accent"][2] - p["bg"][2]) * ratio)
            draw.line(
                [(0, i), (1080, i)],
                fill=(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))),
            )

        for _ in range(150):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(3, 8)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        for i in range(3):
            cx = 540 + random.randint(-100, 100)
            cy = 450 + random.randint(-100, 100)
            r = 80 + i * 40
            draw.ellipse(
                [cx - r, cy - r, cx + r, cy + r], outline=p["secondary"], width=2
            )

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _create_polygon_mesh(self, caption=None):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        points = [(random.randint(0, 1080), random.randint(0, 1080)) for _ in range(50)]

        for i, (x1, y1) in enumerate(points):
            for x2, y2 in points[i + 1 :]:
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < 250:
                    draw.line([x1, y1, x2, y2], fill=p["glow"], width=1)

        for x, y in points:
            size = random.randint(4, 10)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=p["accent"])
            draw.ellipse(
                [x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                fill=p["secondary"],
            )

        for _ in range(100):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(1, 3)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        self._add_header(draw, random.choice(self.HEADER_TITLES), p["accent"])
        if caption:
            self._add_caption_text(draw, caption, p)
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")
        return img

    def _add_header(self, draw, text, color):
        try:
            draw.rectangle([50, 30, 1030, 130], fill=(0, 0, 0, 200))
            bbox = draw.textbbox((0, 0), text, font=self.font_large)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((1080 - text_width) // 2, 45), text, fill=color, font=self.font_large
            )
        except Exception as e:
            logger.warning(f"Header text error: {e}")

    def _add_footer(self, draw, name, url):
        try:
            draw.rectangle([150, 940, 930, 1030], fill=(0, 0, 0, 200))
            bbox = draw.textbbox((0, 0), name, font=self.font_medium)
            name_width = bbox[2] - bbox[0]
            draw.text(
                ((1080 - name_width) // 2, 940),
                name,
                fill=(0, 200, 255),
                font=self.font_medium,
            )

            bbox = draw.textbbox((0, 0), url, font=self.font_small)
            url_width = bbox[2] - bbox[0]
            draw.text(
                ((1080 - url_width) // 2, 985),
                url,
                fill=(100, 180, 200),
                font=self.font_small,
            )
        except Exception as e:
            logger.warning(f"Footer text error: {e}")

    def _add_caption_text(self, draw, caption, palette):
        try:
            y_pos = 170
            lines = caption.split("\n")
            max_width = 980

            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    y_pos += 30
                    continue

                is_title = i == 0 and any(c.isalpha() for c in line)

                if line.startswith("✓"):
                    color = (0, 255, 100)
                    font = self.font_small
                    line = "✓ " + line[1:].strip() if len(line) > 1 else line
                elif is_title:
                    color = palette["accent"]
                    font = self.font_medium
                elif line.replace(" ", "").replace(".", "").isdigit():
                    color = palette["secondary"]
                    font = self.font_small
                elif line.startswith("#") or len(line) <= 3:
                    color = (150, 150, 200)
                    font = self.font_tiny
                    line = line[:35]
                else:
                    color = (255, 255, 255)
                    font = self.font_small

                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]

                if text_width > max_width:
                    words = line.split()
                    lines_wrap = []
                    current_line = ""
                    for word in words:
                        test_line = current_line + " " + word if current_line else word
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        if bbox[2] - bbox[0] <= max_width:
                            current_line = test_line
                        else:
                            if current_line:
                                lines_wrap.append(current_line)
                            current_line = word
                    if current_line:
                        lines_wrap.append(current_line)

                    for j, wrap_line in enumerate(lines_wrap):
                        bbox = draw.textbbox((0, 0), wrap_line, font=font)
                        text_width = bbox[2] - bbox[0]
                        draw.text(
                            ((1080 - text_width) // 2, y_pos),
                            wrap_line,
                            fill=color,
                            font=font,
                        )
                        y_pos += 45
                else:
                    draw.text(
                        ((1080 - text_width) // 2, y_pos), line, fill=color, font=font
                    )
                    y_pos += 45

                y_pos += 8
                if y_pos > 880:
                    break

        except Exception as e:
            logger.warning(f"Caption text error: {e}")

    def _create_simple_fallback(self):
        p = self._get_palette()
        img = Image.new("RGB", (1080, 1080), p["bg"])
        draw = ImageDraw.Draw(img)

        for _ in range(200):
            x, y = random.randint(0, 1080), random.randint(0, 1080)
            size = random.randint(2, 5)
            draw.ellipse([x, y, x + size, y + size], fill=p["glow"])

        draw.rectangle([100, 100, 980, 980], outline=p["accent"], width=5)

        self._add_header(draw, "VAPTANIX", p["accent"])
        self._add_footer(draw, "VAPTANIX", "www.vaptanix.com")

        self.images_dir.mkdir(exist_ok=True)
        image_path = str(
            self.images_dir / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        img.save(image_path, "JPEG", quality=95)

        logger.warning("Using fallback image")
        return image_path, "Vaptanix Security"
