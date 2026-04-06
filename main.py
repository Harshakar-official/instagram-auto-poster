import logging
import sys
from datetime import datetime
import os

from modules.content_generator import ContentGenerator
from modules.image_generator import ImageGenerator
from modules.instagram_poster import InstagramPoster
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("instagram_bot.log"),
    ],
)

logger = logging.getLogger(__name__)


class InstagramBot:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.image_generator = ImageGenerator()
        self.poster = InstagramPoster()

    def create_and_post(self):
        try:
            logger.info("Starting Instagram post creation...")

            logger.info("Generating content (caption + hashtags)...")
            content = self.content_generator.generate_content()
            logger.info(f"Caption: {content['caption']}")
            logger.info(f"Hashtags: {content['hashtags'][:50]}...")

            logger.info("Generating/fetching image...")
            image_path, alt_text = self.image_generator.generate_image()
            logger.info(f"Image saved to: {image_path}")

            logger.info("Posting to Instagram...")
            full_caption = content["full_caption"]
            post_id = self.poster.post(image_path, full_caption)

            if post_id:
                logger.info(f"SUCCESS! Post published with ID: {post_id}")

                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Cleaned up image: {image_path}")

                return {
                    "success": True,
                    "post_id": post_id,
                    "caption": content["caption"],
                    "image_path": image_path,
                }
            else:
                logger.error("FAILED to publish post")
                return {"success": False, "error": "Failed to publish post"}

        except Exception as e:
            logger.error(f"Error in create_and_post: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def get_analytics(self, limit=5):
        try:
            logger.info("Fetching recent posts analytics...")
            posts = self.poster.get_recent_posts(limit)

            analytics = []
            for post in posts:
                insights = self.poster.get_media_insights(post["id"])
                analytics.append(
                    {
                        "id": post.get("id"),
                        "permalink": post.get("permalink"),
                        "timestamp": post.get("timestamp"),
                        "likes": post.get("like_count", 0),
                        "comments": post.get("comments_count", 0),
                        "insights": insights,
                    }
                )

            return analytics

        except Exception as e:
            logger.error(f"Error fetching analytics: {e}")
            return []

    def health_check(self):
        try:
            account_info = self.poster.get_account_info()
            if account_info:
                logger.info(f"Account: {account_info.get('username')}")
                logger.info(f"Media count: {account_info.get('media_count')}")
                return True
            return False
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


def main():
    logger.info("=" * 50)
    logger.info("Instagram Auto-Poster Bot")
    logger.info(f"Started at: {datetime.now()}")
    logger.info(f"Niche: {config.NICHE}")
    logger.info(f"Image Source: {config.IMAGE_SOURCE}")
    logger.info("=" * 50)

    bot = InstagramBot()

    if "--health" in sys.argv:
        if bot.health_check():
            logger.info("Health check passed!")
            sys.exit(0)
        else:
            logger.error("Health check failed!")
            sys.exit(1)

    if "--analytics" in sys.argv:
        analytics = bot.get_analytics()
        for item in analytics:
            logger.info(f"Post: {item['permalink']}")
            logger.info(f"  Likes: {item['likes']}, Comments: {item['comments']}")
        sys.exit(0)

    result = bot.create_and_post()

    if result["success"]:
        logger.info("=" * 50)
        logger.info("POST COMPLETED SUCCESSFULLY!")
        logger.info("=" * 50)
        sys.exit(0)
    else:
        logger.error("=" * 50)
        logger.error(f"POST FAILED: {result.get('error')}")
        logger.error("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
