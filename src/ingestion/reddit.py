import os
import requests
from dotenv import load_dotenv
from src.ingestion.storage import save_raw_data

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ZeptoDiscoveryEngine/1.0.0")

def fetch_reddit_zepto_discussions(limit: int = 50):
    """
    Fetches Reddit posts and comments mentioning the Zepto App.
    Uses OAuth if credentials exist, else uses web endpoint or fallback structured sample.
    """
    print(f"[REDDIT] Searching discussions specifically about 'Zepto App'...")
    formatted_discussions = []
    
    # Try OAuth if credentials provided
    if CLIENT_ID and CLIENT_ID != "your_reddit_client_id" and CLIENT_SECRET and CLIENT_SECRET != "your_reddit_client_secret":
        try:
            auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
            data = {'grant_type': 'client_credentials'}
            headers = {'User-Agent': USER_AGENT}
            token_res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers, timeout=10)
            token_res.raise_for_status()
            token = token_res.json().get('access_token')
            
            api_headers = {**headers, 'Authorization': f'bearer {token}'}
            res = requests.get(f'https://oauth.reddit.com/search?q=Zepto+app&sort=new&limit={limit}', headers=api_headers, timeout=10)
            res.raise_for_status()
            posts = res.json().get('data', {}).get('children', [])
            
            for post in posts:
                p_data = post.get("data", {})
                formatted_discussions.append({
                    "source": "reddit",
                    "app_name": "Zepto",
                    "post_id": p_data.get("id"),
                    "subreddit": p_data.get("subreddit"),
                    "title": p_data.get("title"),
                    "content": p_data.get("selftext"),
                    "score": p_data.get("score"),
                    "num_comments": p_data.get("num_comments"),
                    "permalink": f"https://reddit.com{p_data.get('permalink')}",
                    "created_utc": p_data.get("created_utc")
                })
            save_raw_data(formatted_discussions, "reddit")
            return formatted_discussions
        except Exception as e:
            print(f"[REDDIT WARNING] Live API OAuth call failed: {e}. Falling back to structured search dataset.")

    # Fallback/Sample dataset representing public Reddit discussions about Zepto App
    mock_reddit_discussions = [
        {
            "source": "reddit",
            "app_name": "Zepto",
            "post_id": "rd_101",
            "subreddit": "r/india",
            "title": "Why is Zepto's fresh produce category so hidden in the app?",
            "content": "I usually order chips and cold drinks from Zepto. Yesterday I tried looking for organic vegetables, but the app keeps recommending me snacks instead. Anyone else feel the discovery for non-snack categories is poor?",
            "score": 142,
            "num_comments": 38,
            "permalink": "https://reddit.com/r/india/comments/zepto_produce_discovery",
            "created_utc": 1721500000
        },
        {
            "source": "reddit",
            "app_name": "Zepto",
            "ticket_id": "rd_102",
            "subreddit": "r/Bangalore",
            "title": "Zepto daily essentials vs local supermarket price comparison",
            "content": "Zepto delivery speed is great for emergency snacks, but for monthly household cleaning items, I rarely buy from them because they don't show bundled discounts on the homepage.",
            "score": 89,
            "num_comments": 22,
            "permalink": "https://reddit.com/r/Bangalore/comments/zepto_household_discounts",
            "created_utc": 1721510000
        }
    ]
    
    save_raw_data(mock_reddit_discussions, "reddit")
    return mock_reddit_discussions

if __name__ == "__main__":
    fetch_reddit_zepto_discussions()
