import json
import os
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = "post_state.json"

POSTING_TIMES = [7, 9, 12, 15, 18, 21]


class PostState:
    def __init__(self):
        self.state_file = Path(__file__).parent / STATE_FILE

    def get_last_post_time(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data.get("last_post_time", ""))
            except:
                return None
        return None

    def set_last_post_time(self, post_id=None):
        data = {
            "last_post_time": datetime.now().isoformat(),
            "last_post_id": post_id,
            "version": 1,
        }
        with open(self.state_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_missed_posts(self):
        last_post = self.get_last_post_time()
        now = datetime.now()
        missed = []

        if last_post is None:
            return []

        current_hour = now.hour
        last_hour = last_post.hour

        if now.date() > last_post.date():
            for hour in POSTING_TIMES:
                if hour <= current_hour and hour > 5:
                    missed_dt = now.replace(
                        hour=hour, minute=0, second=0, microsecond=0
                    )
                    if missed_dt > last_post and missed_dt <= now:
                        missed.append(hour)
        elif now.date() == last_post.date():
            for hour in POSTING_TIMES:
                if hour > last_hour and hour <= current_hour:
                    missed.append(hour)

        return missed

    def should_post_now(self):
        last_post = self.get_last_post_time()
        now = datetime.now()

        if last_post is None:
            return True, "No previous post found"

        current_hour = now.hour

        if current_hour in POSTING_TIMES:
            post_time = now.replace(minute=0, second=0, microsecond=0)

            if last_post < post_time:
                time_since = (now - last_post).total_seconds() / 3600
                if time_since >= 1.5:
                    return True, f"Time slot {current_hour}:00 - missed or due"

        return False, f"Last post: {last_post.strftime('%Y-%m-%d %H:%M')}"


if __name__ == "__main__":
    state = PostState()

    print("=" * 50)
    print("POST STATE CHECK")
    print("=" * 50)

    last = state.get_last_post_time()
    if last:
        print(f"Last post: {last.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("No previous posts recorded")

    missed = state.get_missed_posts()
    if missed:
        print(f"MISSED POSTS: {missed}")
    else:
        print("No missed posts")

    should, reason = state.should_post_now()
    print(f"Should post now: {should}")
    print(f"Reason: {reason}")
    print("=" * 50)

    if should and missed:
        print("⚠️  Will post missed content on startup!")
