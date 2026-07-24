import os
from dotenv import load_dotenv
from google_play_scraper import reviews, Sort
from src.ingestion.storage import save_raw_data

load_dotenv()

PACKAGE_NAME = os.getenv("GOOGLE_PLAY_PACKAGE_NAME", "com.zeptoconsumerapp")

def fetch_google_play_reviews(count: int = 200, lang: str = 'en', country: str = 'in'):
    """
    Fetches user reviews specifically for the Zepto App from Google Play Store.
    """
    print(f"[GOOGLE PLAY] Fetching top {count} reviews for package: {PACKAGE_NAME}...")
    try:
        result, _ = reviews(
            PACKAGE_NAME,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=count
        )
        
        formatted_reviews = []
        for r in result:
            formatted_reviews.append({
                "source": "google_play",
                "app_name": "Zepto",
                "review_id": r.get("reviewId"),
                "user_name": r.get("userName"),
                "content": r.get("content"),
                "rating": r.get("score"),
                "thumbs_up": r.get("thumbsUpCount"),
                "created_at": r.get("at").isoformat() if r.get("at") else None,
                "reply_content": r.get("replyContent"),
                "replied_at": r.get("repliedAt").isoformat() if r.get("repliedAt") else None
            })
            
        save_raw_data(formatted_reviews, "google_play")
        return formatted_reviews
    except Exception as e:
        print(f"[GOOGLE PLAY ERROR] Failed to fetch reviews: {e}")
        return []

if __name__ == "__main__":
    fetch_google_play_reviews(count=50)
