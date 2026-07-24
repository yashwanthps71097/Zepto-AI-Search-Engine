import os
import requests
from dotenv import load_dotenv
from src.ingestion.storage import save_raw_data

load_dotenv()

APP_STORE_ID = os.getenv("ZEPTO_APP_STORE_ID", "1582236968")

def fetch_app_store_reviews(country: str = "in"):
    """
    Fetches customer reviews specifically targeting the Zepto App on the Apple App Store using RSS feeds.
    """
    print(f"[APP STORE] Fetching customer reviews for App ID: {APP_STORE_ID}...")
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={APP_STORE_ID}/sortBy=mostRecent/json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        entries = data.get("feed", {}).get("entry", [])
        formatted_reviews = []
        
        for entry in entries:
            # Skip application header entry if present
            if "im:name" in entry and not "author" in entry:
                continue
                
            formatted_reviews.append({
                "source": "app_store",
                "app_name": "Zepto",
                "review_id": entry.get("id", {}).get("label"),
                "author": entry.get("author", {}).get("name", {}).get("label"),
                "title": entry.get("title", {}).get("label"),
                "content": entry.get("content", {}).get("label"),
                "rating": int(entry.get("im:rating", {}).get("label", 0)) if "im:rating" in entry else None,
                "version": entry.get("im:version", {}).get("label") if "im:version" in entry else None
            })
            
        save_raw_data(formatted_reviews, "app_store")
        return formatted_reviews
    except Exception as e:
        print(f"[APP STORE ERROR] Failed to fetch reviews: {e}")
        return []

if __name__ == "__main__":
    fetch_app_store_reviews()
