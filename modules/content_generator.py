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
            "full_caption": f"{caption}\n\n{hashtags}\n\n🔗 Learn more: www.vaptanix.com",
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
        prompt = f"""Generate an educational, engaging Instagram caption about cybersecurity, ethical hacking, or VAPT (Vulnerability Assessment and Penetration Testing). 

Make it:
- Educational and informative
- Professional yet approachable
- Include a relevant emoji
- Between 80-150 characters
- Focus on a specific cybersecurity tip, threat, or insight
- End with a subtle call-to-action or knowledge share

Return ONLY the caption, nothing else."""

        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"

        headers = {
            "Authorization": f"Bearer {self.huggingface_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.8, "top_p": 0.9},
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
                if len(caption) > 30:
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
        templates = [
            "Did you know? 95% of cybersecurity breaches are caused by human error. Regular security training could prevent most attacks. 🛡️",
            "Your password is only as strong as its weakest link. Use a password manager and enable 2FA on all accounts. 🔐",
            "Phishing emails are getting more sophisticated. Always verify sender addresses and never click suspicious links. 🎣",
            "Regular penetration testing can identify vulnerabilities before attackers exploit them. Prevention is better than cure. 🔍",
            "Zero Trust Architecture: Never trust, always verify. In today's threat landscape, assume breach mentality is essential. 🏰",
            "SQL Injection still ranks in top 3 web application vulnerabilities. Always validate and sanitize user inputs. 💉",
            "Ransomware attacks increased 150% last year. Offline backups are your best defense against ransom demands. 💾",
            "Social engineering exploits human psychology, not technical flaws. Security awareness training is your first line of defense. 🧠",
            "Multi-factor authentication prevents 99.9% of account compromises. If you haven't enabled it yet, do it now! ✋",
            "Cloud misconfigurations lead to massive data breaches. Review your cloud settings regularly. ☁️",
            "Buffer overflow vulnerabilities can give attackers full system control. Keep your systems updated and patched. 🛡️",
            "Bug Bounty programs let ethical hackers find vulnerabilities for rewards. It's a win-win for organizations and researchers. 🐛",
            "Data encryption is non-negotiable. Encrypt data at rest and in transit to protect sensitive information. 🔒",
            "Incident response planning is critical. Know what to do BEFORE a breach happens. Time is everything in cybersecurity. ⏰",
            "API security is often overlooked. APIs are prime targets for attackers. Implement rate limiting and authentication. 🔌",
            "Physical security matters too. Tailgating and shoulder surfing are real threats. Stay vigilant in the physical world too. 🚪",
            "Supply chain attacks are rising. Vet your third-party vendors' security practices before integration. ⛓️",
            "Dark web monitoring can alert you if your credentials are compromised. Early detection saves time and money. 🌑",
            "Endpoint detection and response (EDR) is essential for modern security. Traditional antivirus isn't enough anymore. 💻",
            "Security is a shared responsibility. Everyone in an organization plays a role in cybersecurity. 👥",
            "Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages. Always sanitize user input! ⚠️",
            "A firewall is your first line of defense, but it's not enough alone. Layer your security for maximum protection. 🏯",
            "Regular security audits can uncover hidden vulnerabilities. Don't wait for attackers to find them first! 🔎",
            "Mobile apps often have insecure data storage. Check what data your apps are storing on your device. 📱",
            "IoT devices are often the weakest link in network security. Change default passwords and update firmware regularly. 🌐",
            "Brute force attacks try every combination to crack passwords. Use complex, long passwords to make it harder. 🔑",
            "Security patches fix known vulnerabilities. Delayed patching is an open invitation to attackers. ⏳",
            "Phishing isn't just emails anymore - SMS phishing (smishing) and voice phishing (vishing) are on the rise! 📞",
            "Your email is the gateway to your digital life. Protect it with strong authentication and vigilance. 📧",
            "OWASP Top 10 lists the most critical web application security risks. Familiarize yourself with them! 📋",
        ]

        return random.choice(templates)

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
        prompt = """Generate exactly 15 relevant Instagram hashtags for a cybersecurity/VAPT (Vulnerability Assessment and Penetration Testing) company. 

Include a mix of:
- Industry-specific hashtags
- Business-related hashtags
- General security hashtags

Format: #hashtag1 #hashtag2 #hashtag3 etc.

Return ONLY the hashtags, nothing else."""

        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"

        headers = {
            "Authorization": f"Bearer {self.huggingface_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.8},
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
            "cybersecurity": [
                "#cybersecurity",
                "#infosec",
                "#informationsecurity",
                "#pentesting",
                "#ethicalhacking",
                "#vapt",
                "#penetrationtesting",
                "#vulnerabilityassessment",
                "#hacker",
                "#ethicalhacker",
                "#security",
                "#cyberdefense",
                "#cyberattack",
                "#dataprotection",
                "#securityawareness",
                "#infosectips",
                "#cybersafety",
                "#onlinesafety",
                "#privacymatters",
                "#cybercrime",
                "#techsecurity",
                "#networksecurity",
                "#cloudsecurity",
                "#appsec",
                "#websecurity",
            ],
            "tech": [
                "#cybersecurity",
                "#infosec",
                "#informationsecurity",
                "#pentesting",
                "#ethicalhacking",
                "#vapt",
                "#penetrationtesting",
                "#vulnerabilityassessment",
                "#hacker",
                "#ethicalhacker",
                "#security",
                "#cyberdefense",
                "#cyberattack",
                "#dataprotection",
                "#securityawareness",
                "#infosectips",
                "#cybersafety",
                "#onlinesafety",
                "#privacymatters",
                "#cybercrime",
                "#techsecurity",
                "#networksecurity",
                "#cloudsecurity",
                "#appsec",
                "#websecurity",
            ],
        }

        niche_hashtags = hashtag_sets.get(self.niche, hashtag_sets["cybersecurity"])
        selected = random.sample(niche_hashtags, min(15, len(niche_hashtags)))
        return " ".join(selected)
