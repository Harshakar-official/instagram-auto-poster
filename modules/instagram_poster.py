import requests
import logging
import time
import base64
import json
from datetime import datetime
import config
import os

logger = logging.getLogger(__name__)


class InstagramPoster:
    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.ACCESS_TOKEN
        self.base_url = "https://graph.facebook.com/v18.0"

    def upload_to_imgur(self, image_path):
        try:
            with open(image_path, "rb") as file:
                image_data = file.read()

            import urllib.parse

            url = "https://api.imgur.com/3/image"
            headers = {
                "Authorization": "Client-ID c7f5c5e5e5e5e5c7f5c5e5e5e5e5e5c7f5c5e5"
            }
            data = {
                "image": base64.b64encode(image_data).decode("utf-8"),
                "type": "base64",
            }

            response = requests.post(url, headers=headers, data=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get("success"):
                image_url = result["data"]["link"]
                logger.info(f"Uploaded image to imgur: {image_url}")
                return image_url
            else:
                logger.error(f"imgur upload failed: {result}")
                return None

        except Exception as e:
            logger.error(f"Error uploading to imgur: {e}")
            return None

    def create_container(self, image_path, caption):
        try:
            image_url = self.upload_to_imgur(image_path)
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
            logger.error(f"Error uploading to imgbb: {e}")
            return None

    def create_container(self, image_path, caption):
        try:
            image_url = self.upload_to_imgbb(image_path)
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

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating container: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response: {e.response.text}")
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
