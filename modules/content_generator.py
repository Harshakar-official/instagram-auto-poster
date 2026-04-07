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
        content_type = random.choice(
            ["educational", "educational", "educational", "promotional"]
        )

        if content_type == "promotional":
            return self._generate_promo_caption()

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

    def _generate_promo_caption(self):
        promo_templates = [
            "🚀 VAPTANIX SERVICES\n\nProtect your business with professional VAPT!\n\n→ Vulnerability Assessment\n→ Penetration Testing\n→ Security Audits\n→ 24/7 Support\n\nContact us today!\n\n#vaptanix #cybersecurity #pentesting",
            "🔍 NEED A SECURITY CHECK?\n\nYour website might have hidden vulnerabilities.\n\n✓ OWASP Top 10 Testing\n✓ Network Penetration Testing\n✓ Social Engineering Tests\n✓ Full Security Report\n\nGet protected with Vaptanix!\n\n#websitesecurity #pentesting #vapt",
            "💼 ENTERPRISE SECURITY\n\nBig business = big targets.\n\nDon't wait for a breach.\n\n→ Annual Pen Tests\n→ Compliance Ready\n→ Expert Team\n→ Detailed Reports\n\nCall Vaptanix now!\n\n#enterprise #cybersecurity #infosec",
            "🎯 GET HACKED BEFORE HACKERS DO\n\nOur ethical hackers find your weaknesses.\n\n✓ Web App Testing\n✓ API Security\n✓ Mobile App Testing\n✓ Cloud Security\n\nRequest a quote today!\n\n#ethicalhacking #securityaudit #vapt",
            "🛡️ STAY AHEAD OF THREATS\n\nCyber attacks are increasing daily.\n\nAre you protected?\n\n→ Pre-breach Testing\n→ Vulnerability Scans\n→ Security Training\n→ Incident Response\n\nPartner with Vaptanix!\n\n#cybersecurity #threatdetection #security",
            "📞 FREE SECURITY CONSULTATION\n\nNot sure what you need?\n\nWe'll assess your security posture.\n\n✓ No obligation\n✓ Expert advice\n✓ Custom solutions\n✓ Affordable pricing\n\nDM us or visit vaptanix.com\n\n#securityconsultation #cybersecurity",
            "⚡ QUICK VULNERABILITY SCAN\n\nKnow your risks in hours.\n\n→ Automated Scans\n→ Manual Testing\n→ Risk Prioritization\n→ Fix Recommendations\n\nGet started with Vaptanix!\n\n#vulnerabilityscan #cybersecurity #infosec",
            "🏆 TRUST VAPTANIX\n\nProtecting businesses since years.\n\n→ 500+ Tests Completed\n→ 1000+ Vulnerabilities Found\n→ 99% Client Satisfaction\n→ Certified Experts\n\nYour security is our priority!\n\n#vaptanix #trustedsecurity #cybersecurity",
            "🔒 SECURE YOUR SUCCESS\n\nA breach can cost millions.\n\nPrevention costs less.\n\n→ Affordable Plans\n→ Flexible Testing\n→ Detailed Reports\n→ Ongoing Support\n\nContact Vaptanix today!\n\n#prevention #cybersecurity #security",
            "📋 COMPLIANCE MADE EASY\n\nNeed ISO 27001, SOC2, PCI-DSS?\n\nWe help you get there.\n\n→ Gap Analysis\n→ Remediation Support\n→ Audit Preparation\n→ Continuous Monitoring\n\nVaptanix has you covered!\n\n#compliance #isosec #pci #security",
            "🌟 WHY CHOOSE VAPTANIX?\n\n✓ Certified Ethical Hackers\n✓ Latest Tools & Techniques\n✓ Comprehensive Reports\n✓ Affordable Pricing\n✓ Excellent Support\n\nYour trusted security partner!\n\n#vaptanix #ethicalhacker #cybersecurity",
            "💪 PROTECT WHAT MATTERS\n\nYour data, your reputation, your business.\n\nDon't compromise on security.\n\n→ Proactive Testing\n→ Threat Intelligence\n→ Security Awareness\n→ Rapid Response\n\nVaptanix - Your Security Ally!\n\n#dataprotection #cybersecurity #infosec",
            "🎁 LIMITED TIME OFFER\n\nGet 20% OFF on your first VAPT!\n\nComprehensive testing at great price.\n\n→ Network Assessment\n→ Web App Testing\n→ Social Engineering\n→ Detailed Report\n\nHurry! Offer ends soon!\n\n#specialoffer #vapt #cybersecurity",
            "🔐 BEYOND FIREWALLS\n\nFirewalls aren't enough anymore.\n\nYou need comprehensive testing.\n\n✓ External Network Tests\n✓ Internal Network Tests\n✓ WiFi Security\n✓ Physical Security\n\nVaptanix provides complete coverage!\n\n#comprehensivesecurity #vapt #infosec",
            "📱 MOBILE APP SECURITY\n\nApps handle sensitive data.\n\nIs yours secure?\n\n→ iOS & Android Testing\n→ API Security\n→ Data Storage Review\n→ Authentication Tests\n\nGet your app tested by Vaptanix!\n\n#mobileappsec #apps #cybersecurity",
            "☁️ CLOUD SECURITY TESTING\n\nMoving to cloud? Test it!\n\n✓ AWS, Azure, GCP Testing\n✓ Configuration Review\n✓ Access Control Testing\n✓ Data Security\n\nVaptanix - Cloud Security Experts!\n\n#cloudsecurity #aws #azure #cybersecurity",
            "🎓 SECURITY AWARENESS TRAINING\n\nYour employees are your first line of defense.\n\n→ Phishing Simulations\n→ Security Workshops\n→ Best Practices Training\n→ Custom Content\n\nBuild a security-conscious team!\n\n#securitytraining #awareness #cybersecurity",
            "🚨 INCIDENT RESPONSE\n\nBreached? We help!\n\n→ Immediate Assessment\n→ Containment Support\n→ Forensic Analysis\n→ Recovery Planning\n→ Prevention Recommendations\n\nVaptanix IR team is ready 24/7!\n\n#incidentresponse #breach #cybersecurity",
            "💼 STARTUP SECURITY PACKAGE\n\nStartups need security too!\n\nAffordable packages designed for you.\n\n→ Vulnerability Assessment\n→ Basic Pen Testing\n→ Security Consultation\n→ Security Checklist\n\nGet protected from day one!\n\n#startup #entrepreneur #cybersecurity",
            "🔍 RED TEAM ASSESSMENT\n\nThink like an attacker.\n\n✓ Covert Operations\n✓ Social Engineering\n✓ Physical Testing\n✓ Supply Chain Analysis\n\nComprehensive attack simulation by Vaptanix!\n\n#redteam #pentesting #cybersecurity",
        ]

        return random.choice(promo_templates)

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
