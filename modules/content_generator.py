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
            "🔐 PASSWORD SECURITY\n\n95% of breaches start with stolen credentials.\n\n✓ Use 12+ character passwords\n✓ Never reuse passwords\n✓ Enable 2FA everywhere\n✓ Use a password manager\n\n#cybersecurity #infosec #passwordsecurity",
            "🎣 PHISHING ALERT\n\nPhishing accounts for 90% of data breaches!\n\n✓ Check sender email carefully\n✓ Don't click unknown links\n✓ Verify before sharing data\n✓ Report suspicious emails\n\n#phishing #cybersecurity #securityawareness",
            "☁️ CLOUD SECURITY\n\nMisconfigured cloud = exposed data.\n\n✓ Review IAM permissions\n✓ Enable encryption\n✓ Set up logging & monitoring\n✓ Regular security audits\n\n#cloudsecurity #awsecs #cybersecurity",
            "🛡️ ZERO TRUST MODEL\n\n'Never trust, always verify' - the new security standard.\n\n✓ Verify every access request\n✓ Least privilege access\n✓ Assume breach mentality\n✓ Continuous monitoring\n\n#zerotrust #cybersecurity #infosec",
            "💉 SQL INJECTION\n\nStill #1 web vulnerability since 2010!\n\n✓ Use parameterized queries\n✓ Input validation\n✓ Least privilege DB accounts\n✓ Regular security testing\n\n#appsec #sqlinjection #websecurity",
            "💰 RANSOMWARE DEFENSE\n\nAttacks up 150% - are you prepared?\n\n✓ 3-2-1 backup rule\n✓ Offline backups essential\n✓ Never pay the ransom\n✓ Test restore regularly\n\n#ransomware #backupstrategy #cybersecurity",
            "🔍 PENETRATION TESTING\n\nHack yourself before hackers do.\n\n✓ Annual pen testing required\n✓ Cover network, web app, social\n✓ Fix findings quickly\n✓ Document everything\n\n#pentesting #vapt #ethicalhacking",
            "📱 MOBILE SECURITY\n\nYour phone = your digital identity.\n\n✓ Lock with biometrics\n✓ Review app permissions\n✓ Avoid public WiFi\n✓ Keep OS updated\n\n#mobilesecurity #privacymatters #cybersecurity",
            "🧠 SOCIAL ENGINEERING\n\nHumans are the weakest link.\n\n✓ Regular security training\n✓ Phishing simulations\n✓ Clear reporting procedures\n✓ Security culture matters\n\n#socialengineering #securityawareness #infosec",
            "🔒 DATA ENCRYPTION\n\nYour data's armor against theft.\n\n✓ Encrypt at rest & in transit\n✓ Use strong encryption (AES-256)\n✓ Manage keys properly\n✓ Key rotation is critical\n\n#encryption #dataprotection #cybersecurity",
            "⛓️ SUPPLY CHAIN SECURITY\n\nYour security = weakest vendor's security.\n\n✓ Vet all vendors thoroughly\n✓ Include security requirements\n✓ Regular vendor assessments\n✓ Have exit strategies\n\n#supplychain #thirdpartyrisk #cybersecurity",
            "💻 ENDPOINT SECURITY\n\nEvery device is a potential entry point.\n\n✓ EDR not just antivirus\n✓ Zero trust endpoints\n✓ Regular patching\n✓ Monitor for anomalies\n\n#endpointsecurity #edr #cybersecurity",
            "🔑 API SECURITY\n\nAPIs are attackers' favorite target.\n\n✓ Authenticate all requests\n✓ Rate limiting essential\n✓ Validate all inputs\n✓ API gateways help\n\n#apisecurity #devsecops #infosec",
            "🚪 PHYSICAL SECURITY\n\nDigital security starts physical.\n\n✓ Badge access control\n✓ Clean desk policy\n✓ Screen locks mandatory\n✓ CCTV & monitoring\n\n#physicalsecurity #securityculture #cybersecurity",
            "📊 INCIDENT RESPONSE\n\nHow you respond matters most.\n\n✓ Have a written IR plan\n✓ Practice regularly\n✓ Document everything\n✓ Learn from incidents\n\n#incidentresponse #IR #cybersecurity",
            "🌐 IoT SECURITY\n\nSmart devices = smart risks.\n\n✓ Change default passwords\n✓ Update firmware regularly\n✓ Network segmentation\n✓ Disable unused features\n\n#iotsecurity #smarthome #cybersecurity",
            "🔍 DARK WEB MONITORING\n\nYour data might already be sold.\n\n✓ Monitor for leaked creds\n✓ Brand monitoring\n✓ Early detection = less damage\n✓ Have response ready\n\n#darkweb #threatintel #cybersecurity",
            "📧 EMAIL SECURITY\n\nEmail = #1 attack vector.\n\n✓ DMARC, SPF, DKIM setup\n✓ Phishing filters\n✓ Links inspection tools\n✓ User training essential\n\n#emailsecurity #phishing #infosec",
            "🏰 DEFENSE IN DEPTH\n\nOne layer isn't enough.\n\n✓ Multiple security layers\n✓ Network segmentation\n✓ Access controls everywhere\n✓ Monitor all layers\n\n#defenseindepth #layeredsecurity #cybersecurity",
            "🐛 BUG BOUNTY\n\nLet hackers find bugs for you.\n\n✓ Crowdsourced security\n✓ Reward researchers\n✓ Fix issues fast\n✓ Public programs work\n\n#bugbounty #ethicalhacking #infosec",
            "🔄 PATCH MANAGEMENT\n\nUnpatched = compromised.\n\n✓ Automate where possible\n✓ Prioritize critical patches\n✓ Test before deployment\n✓ Track all assets\n\n#patchmanagement #vulnerabilities #cybersecurity",
            "📋 OWASP TOP 10\n\nThe web security bible.\n\n✓ Know all 10 risks\n✓ Regular security training\n✓ Code review essential\n✓ Test against OWASP\n\n#owasp #websecurity #appsec",
            "👥 SECURITY CULTURE\n\nSecurity is everyone's job.\n\n✓ Lead by example\n✓ Make it engaging\n✓ Reward good behavior\n✓ Continuous learning\n\n#securityculture #employees #cybersecurity",
            "📈 THREAT INTELLIGENCE\n\nKnow your enemy.\n\n✓ Monitor threat feeds\n✓ Understand TTPs\n✓ Share intel internally\n✓ Act on intelligence\n\n#threatintelligence #cybersecurity #infosec",
            "☠️ MALWARE TYPES\n\nRansomware, trojans, botnets, APTs...\n\n✓ Know the threats\n✓ Multi-vector protection\n✓ User awareness\n✓ Quick detection\n\n#malware #ransomware #cybersecurity",
            "🔐 MFA BENEFITS\n\n2FA stops 99.9% of attacks!\n\n✓ Something you know\n✓ Something you have\n✓ Something you are\n✓ Use authenticator apps\n\n#MFA #2FA #authentication",
            "🛑 FIREWALL BASICS\n\nYour network's first defense.\n\n✓ Whitelist over blacklist\n✓ Default deny\n✓ Log everything\n✓ Regular review\n\n#firewall #networksecurity #cybersecurity",
            "📊 SECURITY AUDIT\n\nCan't protect what you can't see.\n\n✓ Annual comprehensive audit\n✓ Penetration testing\n✓ Compliance checks\n✓ Gap analysis\n\n#securityaudit #compliance #cybersecurity",
            "🌍 REMOTE WORK SECURITY\n\nHome = new security perimeter.\n\n✓ VPN mandatory\n✓ Secure home network\n✓ Device encryption\n✓ Separation of work/personal\n\n#remotework #cybersecurity #infosec",
            "💡 SECURITY BY DESIGN\n\nSecurity built in vs bolted on.\n\n✓ SDLC integration\n✓ Threat modeling\n✓ Secure defaults\n✓ Minimize attack surface\n\n#securitybydesign #devsecops #cybersecurity",
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
