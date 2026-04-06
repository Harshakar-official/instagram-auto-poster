import requests
import logging
import time
import base64
from datetime import datetime
import config
import os

logger = logging.getLogger(__name__)


class InstagramPoster:
    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.ACCESS_TOKEN
        self.base_url = "https://graph.facebook.com/v18.0"

    def upload_to_catbox(self, image_path):
        try:
            with open(image_path, "rb") as file:
                files = {
                    "reqtype": (None, "fileupload"),
                    "time": (None, "72h"),
                    "fileToUpload": file,
                }
                response = requests.post(
                    "https://catbox.moe/user/api.php", files=files, timeout=120
                )

            if response.status_code == 200:
                image_url = response.text.strip()
                if image_url.startswith("https://"):
                    logger.info(f"Uploaded to catbox: {image_url}")
                    return image_url
            return None
        except Exception as e:
            logger.error(f"catbox upload failed: {e}")
            return None

    def upload_to_0x0_st(self, image_path):
        try:
            with open(image_path, "rb") as file:
                files = {"file": file}
                response = requests.post("https://0x0.st", files=files, timeout=60)

            response.raise_for_status()
            image_url = response.text.strip()
            logger.info(f"Uploaded to 0x0.st: {image_url}")
            return image_url

        except Exception as e:
            logger.error(f"0x0.st upload failed: {e}")
            return None

    def upload_to_litterbox(self, image_path):
        try:
            with open(image_path, "rb") as file:
                files = {
                    "reqtype": (None, "fileupload"),
                    "time": (None, "72h"),
                    "fileToUpload": file,
                }
                response = requests.post(
                    "https://litterbox.catbox.moe/resources/internals/api.php",
                    files=files,
                    timeout=60,
                )

            if response.status_code == 200:
                image_url = response.text.strip()
                if image_url.startswith("https://"):
                    logger.info(f"Uploaded to litterbox: {image_url}")
                    return image_url
            return None
        except Exception as e:
            logger.error(f"Litterbox upload failed: {e}")
            return None

    def upload_to_tmpfiles(self, image_path):
        try:
            with open(image_path, "rb") as file:
                files = {"file": ("image.jpg", file, "image/jpeg")}
                response = requests.post(
                    "https://tmpfiles.org/api/v1/upload", files=files, timeout=60
                )

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    url = data.get("data", {}).get("url", "")
                    image_url = url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                    logger.info(f"Uploaded to tmpfiles: {image_url}")
                    return image_url
            return None
        except Exception as e:
            logger.error(f"tmpfiles upload failed: {e}")
            return None

    def upload_image(self, image_path):
        services = [
            ("Catbox", self.upload_to_catbox),
            ("Litterbox", self.upload_to_litterbox),
            ("0x0.st", self.upload_to_0x0_st),
            ("tmpfiles", self.upload_to_tmpfiles),
        ]

        for name, func in services:
            try:
                image_url = func(image_path)
                if image_url:
                    logger.info(f"Successfully uploaded via {name}")
                    return image_url
            except Exception as e:
                logger.error(f"{name} failed: {e}")

        logger.error("All image hosting services failed")
        return None

    def create_container(self, image_path, caption):
        try:
            image_url = self.upload_image(image_path)
            if not image_url:
                logger.error("Failed to upload image, cannot create container")
                return None

            url = f"{self.base_url}/{self.user_id}/media"

            data = {
                "caption": caption,
                "image_url": image_url,
                "access_token": self.access_token,
            }

            response = requests.post(url, data=data, timeout=60)
            response.raise_for_status()

            result = response.json()

            if "id" in result:
                container_id = result["id"]
                logger.info(f"Created media container: {container_id}")
                return container_id
            else:
                logger.error(f"No container ID in response: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating container: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

        except Exception as e:
            logger.error(f"Error creating container: {e}")
            return None

    def publish_container(self, container_id):
        try:
            url = f"{self.base_url}/{self.user_id}/media_publish"

            data = {"creation_id": container_id, "access_token": self.access_token}

            response = requests.post(url, data=data, timeout=60)
            response.raise_for_status()

            result = response.json()

            if "id" in result:
                post_id = result["id"]
                logger.info(f"Published post successfully: {post_id}")
                return post_id
            else:
                logger.error(f"No post ID in response: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error publishing container: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

    def post(self, image_path, caption, max_retries=None):
        if max_retries is None:
            max_retries = config.MAX_RETRIES

        if max_retries <= 0:
            max_retries = 3

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to post (attempt {attempt + 1}/{max_retries})")

                container_id = self.create_container(image_path, caption)
                if not container_id:
                    logger.warning(
                        f"Failed to create container on attempt {attempt + 1}"
                    )
                    if attempt < max_retries - 1:
                        time.sleep(config.RETRY_DELAY)
                        continue
                    return None

                time.sleep(3)

                post_id = self.publish_container(container_id)
                if not post_id:
                    logger.warning(f"Failed to publish on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        time.sleep(config.RETRY_DELAY)
                        continue
                    return None

                logger.info(f"Successfully posted! Post ID: {post_id}")
                return post_id

            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(config.RETRY_DELAY)

        logger.error(f"Failed to post after {max_retries} attempts")
        return None

    def get_account_info(self):
        try:
            url = f"{self.base_url}/{self.user_id}"

            params = {
                "fields": "id,username, name, media_count, followers_count, follows_count",
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting account info: {e}")
            return None

    def get_media_insights(self, media_id):
        try:
            url = f"{self.base_url}/{media_id}"

            params = {
                "fields": "id,caption,media_type,permalink,timestamp,like_count,comments_count,impressions,reach,saved",
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting media insights: {e}")
            return None

    def get_recent_posts(self, limit=10):
        try:
            url = f"{self.base_url}/{self.user_id}/media"

            params = {
                "fields": "id,caption,media_type,permalink,timestamp,like_count,comments_count",
                "limit": limit,
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get("data", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
