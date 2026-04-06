import requests
import logging
import json
import random
import config

logger = logging.getLogger(__name__)


class ContentGenerator:
    def __init__(self):
        self.niche = config.NICHE
        self.huggingface_token = config.HUGGINGFACE_TOKEN
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"

    def generate_content(self):
        caption = self._generate_caption()
        hashtags = self._generate_hashtags()

        return {
            "caption": caption,
            "hashtags": hashtags,
            "full_caption": f"{caption}\n\n{hashtags}",
        }

    def _generate_caption(self):
        try:
            if self.huggingface_token:
                return self._generate_with_huggingface()
            else:
                return self._generate_template_caption()
        except Exception as e:
            logger.error(f"Caption generation error: {e}")
            return self._generate_template_caption()

    def _generate_with_huggingface(self):
        prompts = {
            "food": """Generate an engaging Instagram caption about food. Make it descriptive, appetizing, and include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "travel": """Generate an exciting Instagram caption about travel and adventure. Make it inspiring and wanderlust-inducing. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "fitness": """Generate a motivating Instagram caption about fitness and health. Make it energetic and inspiring. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "fashion": """Generate a stylish Instagram caption about fashion. Make it chic and trendy. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "tech": """Generate a clever Instagram caption about technology. Make it smart and engaging. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "lifestyle": """Generate a warm Instagram caption about lifestyle and everyday moments. Make it relatable and genuine. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "nature": """Generate a beautiful Instagram caption about nature. Make it peaceful and awe-inspiring. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "business": """Generate an inspiring Instagram caption about business and success. Make it motivational and professional. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "art": """Generate a creative Instagram caption about art and creativity. Make it artistic and expressive. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
            "photography": """Generate an artistic Instagram caption about photography. Make it visual and creative. Include an emoji. Keep it between 50-150 characters. Return ONLY the caption, nothing else.""",
        }

        prompt = prompts.get(self.niche, prompts["lifestyle"])

        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"

        headers = {
            "Authorization": f"Bearer {self.huggingface_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 100, "temperature": 0.8, "top_p": 0.9},
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=60)

            if response.status_code == 503:
                logger.warning("HuggingFace model loading, falling back to templates")
                return self._generate_template_caption()

            if response.status_code == 429:
                logger.warning("HuggingFace rate limit, falling back to templates")
                return self._generate_template_caption()

            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                caption = result[0].get("generated_text", "").strip()
                caption = caption.split("\n")[0].strip()
                if len(caption) > 20:
                    logger.info("Generated caption with Hugging Face")
                    return caption
            elif isinstance(result, dict) and "error" in result:
                logger.warning(f"HuggingFace API error: {result['error']}")
                return self._generate_template_caption()

        except requests.exceptions.RequestException as e:
            logger.warning(f"HuggingFace request failed: {e}")
            return self._generate_template_caption()

        return self._generate_template_caption()

    def _generate_template_caption(self):
        templates = {
            "food": [
                "Satisfying my cravings today! 🍽️✨",
                "Good food, good mood! 😋",
                "Because pizza is always the answer! 🍕",
                "Feeding my soul one bite at a time 🥄",
                "Life is short, eat dessert first! 🍰",
            ],
            "travel": [
                "Collecting moments, not things 🌍✈️",
                "Adventure awaits around every corner 🗺️",
                "Lost in the beauty of this place 🌅",
                "Making memories one destination at a time 📸",
                "The world is calling and I must go 🌍",
            ],
            "fitness": [
                "Sweat is just fat crying 💪🔥",
                "Push yourself because no one else will 🏋️",
                "The only bad workout is the one that didn't happen ⚡",
                "Strong is the new beautiful 💪✨",
                "Train insane or remain the same 🔥",
            ],
            "fashion": [
                "Style is a way to say who you are without speaking 👗✨",
                "Dress like you're going to meet your worst enemy 👠",
                "Fashion is the armor to survive the reality of everyday life 👗",
                "When you look good, you feel good 💅",
                "Elegance is refusal 🖤",
            ],
            "tech": [
                "The future is now 🤖✨",
                "Innovation distinguishes between a leader and a follower 💡",
                "Code is poetry in motion 💻",
                "Building the future, one line at a time 🚀",
                "Simplicity is the ultimate sophistication 📱",
            ],
            "lifestyle": [
                "Creating a life I love 💫",
                "The best is yet to come ✨",
                "Living my best life 🌟",
                "Making every day count ☀️",
                "Chasing dreams and coffee mugs ☕",
            ],
            "nature": [
                "Nature does not hurry, yet everything is accomplished 🍃",
                "In every walk with nature, one receives far more than he seeks 🌿",
                "The earth has music for those who listen 🎋",
                "Breathtaking views at every turn 🌄",
                "Where nature meets tranquility 🌸",
            ],
            "business": [
                "Success is not final, failure is not fatal 🏆",
                "Dream bigger, work harder 💼",
                "Building empires, one day at a time 👑",
                "The grind doesn't stop 💪",
                "Think big, achieve bigger 📈",
            ],
            "art": [
                "Art is not what you see, but what you make others see 🎨",
                "Every artist was first an amateur 🖌️",
                "Creativity takes courage ✨",
                "Art speaks where words fail to 💫",
                "Making the ordinary extraordinary 🎭",
            ],
            "photography": [
                "Capturing moments, creating memories 📸",
                "The best thing about a picture is that it never changes 📷",
                "Life in focus 🎯",
                "Seeing the world through a different lens 👁️",
                "Moments captured, stories told 🖼️",
            ],
        }

        niche_templates = templates.get(self.niche, templates["lifestyle"])
        return random.choice(niche_templates)

    def _generate_hashtags(self):
        try:
            if self.huggingface_token:
                return self._generate_hashtags_with_ai()
            else:
                return self._generate_template_hashtags()
        except Exception as e:
            logger.error(f"Hashtag generation error: {e}")
            return self._generate_template_hashtags()

    def _generate_hashtags_with_ai(self):
        prompt = f"""Generate exactly 15 Instagram hashtags for a {self.niche} themed post. Format: #hashtag1 #hashtag2 etc. Make them popular and relevant. Return ONLY the hashtags, nothing else."""

        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"

        headers = {
            "Authorization": f"Bearer {self.huggingface_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 100, "temperature": 0.8},
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=60)

            if response.status_code == 503:
                logger.warning("HuggingFace model loading, falling back to templates")
                return self._generate_template_hashtags()

            if response.status_code == 429:
                logger.warning("HuggingFace rate limit, falling back to templates")
                return self._generate_template_hashtags()

            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                hashtags_text = result[0].get("generated_text", "").strip()
                hashtags = self._parse_hashtags(hashtags_text)
                if len(hashtags) >= 10:
                    logger.info("Generated hashtags with Hugging Face")
                    return " ".join(hashtags[:15])
            elif isinstance(result, dict) and "error" in result:
                logger.warning(f"HuggingFace API error: {result['error']}")
                return self._generate_template_hashtags()

        except requests.exceptions.RequestException as e:
            logger.warning(f"HuggingFace request failed: {e}")
            return self._generate_template_hashtags()

        return self._generate_template_hashtags()

    def _parse_hashtags(self, text):
        import re

        hashtags = re.findall(r"#\w+", text)
        return hashtags

    def _generate_template_hashtags(self):
        hashtag_sets = {
            "food": [
                "#foodie",
                "#foodporn",
                "#foodphotography",
                "#instafood",
                "#yummy",
                "#delicious",
                "#foodstagram",
                "#foodblogger",
                "#foodlover",
                "#homemade",
                "#healthyfood",
                "#foodgasm",
                "#breakfast",
                "#lunch",
                "#dinner",
                "#snack",
                "#cuisine",
                "#foodstyling",
                "#tasty",
                "#nomnom",
            ],
            "travel": [
                "#travel",
                "#travelgram",
                "#travelphotography",
                "#wanderlust",
                "#explore",
                "#adventure",
                "#travelblogger",
                "#instatravel",
                "#traveling",
                "#traveler",
                "#vacation",
                "#holiday",
                "#travelling",
                "#getaway",
                "#trip",
                "#tourism",
                "#landscape",
                "#nature",
                "#discovery",
                "#passport",
            ],
            "fitness": [
                "#fitness",
                "#fitnessmotivation",
                "#gym",
                "#workout",
                "#fit",
                "#fitnessjourney",
                "#training",
                "#health",
                "#fitnesslife",
                "#bodybuilding",
                "#motivation",
                "#fitfam",
                "#strength",
                "#healthylifestyle",
                "#exercise",
                "#gymlife",
                "#crossfit",
                "#yoga",
                "#running",
                "#weightlifting",
            ],
            "fashion": [
                "#fashion",
                "#style",
                "#ootd",
                "#fashionblogger",
                "#instafashion",
                "#fashionista",
                "#stylish",
                "#clothing",
                "#outfit",
                "#fashionstyle",
                "#streetstyle",
                "#look",
                "#trend",
                "#fashionable",
                "#wardrobe",
                "#closet",
                "#outfitoftheday",
                "#instastyle",
                "#fashionaddict",
                "#styleinspo",
            ],
            "tech": [
                "#tech",
                "#technology",
                "#innovation",
                "#programming",
                "#coding",
                "#developer",
                "#software",
                "#ai",
                "#technews",
                "#gadget",
                "#startup",
                "#digital",
                "#cybersecurity",
                "#datascience",
                "#machinelearning",
                "#python",
                "#webdevelopment",
                "#app",
                "#techlover",
                "#futuretech",
            ],
            "lifestyle": [
                "#lifestyle",
                "#life",
                "#instagood",
                "#happy",
                "#love",
                "#beautiful",
                "#motivation",
                "#inspiration",
                "#lifestyleblogger",
                "#livemusic",
                "#goodvibes",
                "#positivevibes",
                "#mindfulness",
                "#selfcare",
                "#wellness",
                "# positivity",
                "#goals",
                "#dreams",
                "#success",
                "#happiness",
            ],
            "nature": [
                "#nature",
                "#naturephotography",
                "#landscape",
                "#photooftheday",
                "#beautiful",
                "#sky",
                "#sunset",
                "#mountains",
                "#ocean",
                "#flowers",
                "#wildlife",
                "#forest",
                "#sunrise",
                "#travel",
                "#tree",
                "#green",
                "# scenery",
                "#naturelovers",
                "#earth",
                "#outdoors",
            ],
            "business": [
                "#business",
                "#entrepreneur",
                "#success",
                "#motivation",
                "#money",
                "#marketing",
                "#investment",
                "#startup",
                "#ceo",
                "#hustle",
                "#leadership",
                "#businessowner",
                "#smallbusiness",
                "#growth",
                "#goals",
                "#wealth",
                "#entrepreneurship",
                "#successquotes",
                "#businessmindset",
                "#workhard",
            ],
            "art": [
                "#art",
                "#artist",
                "#artwork",
                "#painting",
                "#drawing",
                "#illustration",
                "#creative",
                "#design",
                "#artistic",
                "#instaart",
                "#artoftheday",
                "#beautiful",
                "#contemporaryart",
                "#photography",
                "#digitalart",
                "#sketch",
                "#artgallery",
                "#fineart",
                "#modernart",
                "#gallery",
            ],
            "photography": [
                "#photography",
                "#photooftheday",
                "#photographer",
                "#photoshoot",
                "#instaphoto",
                "#portrait",
                "#landscape",
                "#naturephotography",
                "#streetphotography",
                "#camera",
                "#shotoniphone",
                "#photo",
                "#picoftheday",
                "#igphotography",
                "#photographylovers",
                "#canon",
                "#nikon",
                "#dslr",
                "#visualsoflife",
                "#artofvisuals",
            ],
        }

        niche_hashtags = hashtag_sets.get(self.niche, hashtag_sets["lifestyle"])
        selected = random.sample(niche_hashtags, min(15, len(niche_hashtags)))
        return " ".join(selected)
