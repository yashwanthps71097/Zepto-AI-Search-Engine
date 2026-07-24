import os
import requests
from dotenv import load_dotenv
from src.ingestion.storage import save_raw_data

load_dotenv()

def fetch_social_media_mentions():
    """
    Fetches public social media posts/tweets and social listening data 
    specifically mentioning the Zepto App (Twitter/X, public forums, brand mentions).
    """
    print("[SOCIAL MEDIA] Ingesting social media posts and mentions for 'Zepto App'...")
    
    # In production, this integrates with Twitter/X v2 API or Brandwatch/Meltwater endpoints.
    # Below is the structured ingestion schema capturing social media feedback.
    social_posts = [
        {
            "source": "twitter_x",
            "app_name": "Zepto",
            "post_id": "tw_201",
            "author_handle": "@tech_shopper_in",
            "content": "Zepto's 10-minute delivery is fast, but why doesn't the app recommend gourmet coffee when I buy milk every morning? Missed cross-selling opportunity! #ZeptoApp",
            "likes": 45,
            "retweets": 12,
            "created_at": "2026-07-20T14:20:00Z"
        },
        {
            "source": "twitter_x",
            "app_name": "Zepto",
            "post_id": "tw_202",
            "author_handle": "@delhi_foodie",
            "content": "Lately I noticed Zepto added a new bakery section, but it's buried under 3 sub-menus in the app. Had to search manually. Fix your catalog UI! @ZeptoNow",
            "likes": 110,
            "retweets": 28,
            "created_at": "2026-07-21T08:10:00Z"
        }
    ]
    
    save_raw_data(social_posts, "social_media")
    return social_posts

if __name__ == "__main__":
    fetch_social_media_mentions()
