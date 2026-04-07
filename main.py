import logging
import sys
import time
import schedule
from datetime import datetime
import os
from pathlib import Path
from threading import Thread

from modules.content_generator import ContentGenerator
from modules.image_generator import ImageGenerator
from modules.instagram_poster import InstagramPoster
from post_state import PostState
import config

LOG_DIR = Path("/Users/harshakar/Documents/Instagram Automation")
LOG_FILE = LOG_DIR / "instagram_bot.log"

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE)),
    ],
)

logger = logging.getLogger(__name__)


class InstagramBot:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.image_generator = ImageGenerator()
        self.poster = InstagramPoster()

    def create_and_post(self, use_ai_image=False):
        try:
            logger.info("=" * 50)
            logger.info("Starting Instagram post creation...")
            logger.info("=" * 50)

            logger.info("Generating content (caption + hashtags)...")
            content = self.content_generator.generate_content()
            logger.info(f"Caption: {content['caption'][:100]}...")
            logger.info(f"Hashtags: {content['hashtags'][:80]}...")

            if use_ai_image or config.USE_AI_IMAGES:
                logger.info("Generating AI image using Pollinations.ai (FREE)...")
                ai_image_path = self.image_generator.generate_ai_image(
                    content["caption"]
                )
                if ai_image_path:
                    image_path = ai_image_path
                    logger.info(f"AI Image saved to: {image_path}")
                else:
                    logger.warning("AI image failed, falling back to infographic...")
                    image_path, alt_text = self.image_generator.generate_image(
                        content["caption"]
                    )
            else:
                logger.info("Generating infographic image with text...")
                image_path, alt_text = self.image_generator.generate_image(
                    content["caption"]
                )

            logger.info(f"Image saved to: {image_path}")

            logger.info("Posting to Instagram...")
            full_caption = content["full_caption"]
            post_id = self.poster.post(image_path, full_caption)

            if post_id:
                logger.info("=" * 50)
                logger.info(f"SUCCESS! Post published with ID: {post_id}")
                logger.info("=" * 50)

                post_state = PostState()
                post_state.set_last_post_time(post_id)
                logger.info("Post state updated")

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
                logger.info(f"Followers: {account_info.get('followers_count', 'N/A')}")
                return True
            return False
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


def run_scheduler():
    schedule.every().day.at("07:00").do(run_post)
    schedule.every().day.at("09:00").do(run_post)
    schedule.every().day.at("12:00").do(run_post)
    schedule.every().day.at("15:00").do(run_post)
    schedule.every().day.at("18:00").do(run_post)
    schedule.every().day.at("21:00").do(run_post)

    logger.info(
        "Scheduler started! Posts will run at 7AM, 9AM, 12PM, 3PM, 6PM, and 9PM daily"
    )
    logger.info("Press Ctrl+C to stop")

    while True:
        schedule.run_pending()
        time.sleep(60)


def run_post():
    bot = InstagramBot()
    use_ai = "--ai" in sys.argv or config.USE_AI_IMAGES
    result = bot.create_and_post(use_ai_image=use_ai)
    if result["success"]:
        logger.info("Scheduled post completed successfully!")
    else:
        logger.error("Scheduled post failed!")


def main():
    logger.info("=" * 60)
    logger.info("   VAPTANIX Instagram Auto-Poster")
    logger.info("   Cybersecurity Content Automation")
    logger.info("=" * 60)
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Niche: {config.NICHE}")
    logger.info("=" * 60)

    bot = InstagramBot()

    if "--health" in sys.argv:
        logger.info("Running health check...")
        if bot.health_check():
            logger.info("Health check passed! Everything is working!")
            sys.exit(0)
        else:
            logger.error("Health check failed!")
            sys.exit(1)

    if "--analytics" in sys.argv:
        logger.info("Fetching analytics...")
        analytics = bot.get_analytics()
        if analytics:
            logger.info("\n" + "=" * 50)
            logger.info("RECENT POSTS ANALYTICS")
            logger.info("=" * 50)
            for i, item in enumerate(analytics, 1):
                logger.info(f"\n{i}. {item['permalink']}")
                logger.info(f"   Likes: {item['likes']} | Comments: {item['comments']}")
                logger.info(f"   Posted: {item['timestamp']}")
        else:
            logger.info("No posts found or failed to fetch analytics")
        sys.exit(0)

    if "--schedule" in sys.argv:
        logger.info("Starting scheduler mode...")
        run_scheduler()

    if "--post" in sys.argv or len(sys.argv) == 1:
        use_ai = "--ai" in sys.argv
        logger.info("Creating and posting now...")
        if use_ai:
            logger.info("AI image generation: ENABLED")
        result = bot.create_and_post(use_ai_image=use_ai)

        if result["success"]:
            logger.info("\n" + "=" * 60)
            logger.info("   POST COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info(f"Post ID: {result['post_id']}")
            logger.info(f"Caption: {result['caption']}")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.error("\n" + "=" * 60)
            logger.error("   POST FAILED!")
            logger.error("=" * 60)
            logger.error(f"Error: {result.get('error')}")
            logger.error("=" * 60)
            sys.exit(1)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           VAPTANIX Instagram Auto-Poster                 ║
    ║           Cybersecurity Content Automation               ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Commands:
    python main.py           - Post now (infographic style)
    python main.py --post    - Post now (infographic style)
    python main.py --ai      - Post with AI-generated image (FREE!)
    python main.py --health  - Check if connected
    python main.py --analytics - View post stats
    python main.py --schedule - Auto-post daily (6x/day)
    python main.py --schedule --ai - Auto-post with AI images
    
    Environment Variables:
    USE_AI_IMAGES=true       - Enable AI images by default
    
    """)
    main()
