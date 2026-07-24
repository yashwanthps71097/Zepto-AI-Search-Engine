import os
import json
from pathlib import Path
from src.ingestion.storage import save_raw_data

def fetch_youtube_reviews():
    """
    Simulates fetching video reviews for Zepto app.
    URL: https://www.youtube.com/results?search_query=Zepto+review
    """
    mock_reviews = [
        {
            "id": "yt_1",
            "source": "YouTube",
            "url": "https://www.youtube.com/watch?v=mock1",
            "author": "TechVlogIndia",
            "content": "Zepto grocery delivery is super fast, but why is pet food so expensive here compared to my local pet store? I'd rather buy groceries here and buy dog food offline.",
            "sentiment": "neutral",
            "barrier": "HIGH_PRICE"
        },
        {
            "id": "yt_2",
            "source": "YouTube",
            "url": "https://www.youtube.com/watch?v=mock2",
            "author": "QuickCommCritic",
            "content": "Tested Zepto's Gourmet cheese block. The quality is fine, but they only sell a 500g block. Why can't we get smaller trial sizes for gourmet cheese?",
            "sentiment": "negative",
            "barrier": "PACK_SIZE_TOO_LARGE"
        }
    ]
    save_raw_data(mock_reviews, "youtube")
    return mock_reviews

def fetch_quora_discussions():
    """
    Simulates fetching Quora discussions.
    URL: https://www.quora.com/search?q=Zepto
    """
    mock_reviews = [
        {
            "id": "quora_1",
            "source": "Quora",
            "content": "Why is the organic produce section so hard to find in the Zepto UI? I had to search multiple times to find organic apples. It's hidden in sub-menus.",
            "sentiment": "negative",
            "barrier": "HIDDEN_IN_UI"
        }
    ]
    save_raw_data(mock_reviews, "quora")
    return mock_reviews

def fetch_linkedin_articles():
    """
    Simulates fetching LinkedIn quick commerce discussions.
    URL: https://www.linkedin.com/search/results/content/?keywords=quick%20commerce
    """
    mock_reviews = [
        {
            "id": "linkedin_1",
            "source": "LinkedIn",
            "content": "Zepto's rapid delivery speed creates a strict habit loop. Users complete orders for daily bread & milk in 30 seconds, completely bypassing new categories.",
            "sentiment": "neutral",
            "barrier": "HABIT_LOOP"
        }
    ]
    save_raw_data(mock_reviews, "linkedin")
    return mock_reviews

def fetch_product_hunt_feedback():
    """
    Simulates Product Hunt feedback.
    URL: https://www.producthunt.com/search?q=Zepto
    """
    mock_reviews = [
        {
            "id": "ph_1",
            "source": "Product Hunt",
            "content": "Love the UI layout but would love a quick 'Add Trial Pack' button directly on checkout for organic veggies and premium snacks.",
            "sentiment": "positive",
            "barrier": "HIDDEN_IN_UI"
        }
    ]
    save_raw_data(mock_reviews, "product_hunt")
    return mock_reviews

def fetch_mouthshut_reviews():
    """
    Simulates MouthShut reviews.
    URL: https://www.mouthshut.com/product-reviews/Zepto-10-Minute-Grocery-Delivery-reviews-926105342
    """
    mock_reviews = [
        {
            "id": "mouthshut_1",
            "source": "MouthShut",
            "content": "Zepto delivers in 10 mins but fruits are sometimes stale. Need a quality guarantee badge before trying organic fruits.",
            "sentiment": "negative",
            "barrier": "QUALITY_CONCERN"
        }
    ]
    save_raw_data(mock_reviews, "mouthshut")
    return mock_reviews

def fetch_trustpilot_reviews():
    """
    Simulates Trustpilot reviews.
    URL: https://www.trustpilot.com/review/www.zeptonow.com
    """
    mock_reviews = [
        {
            "id": "trustpilot_1",
            "source": "Trustpilot",
            "content": "Great customer service when organic produce freshness was off. Refund was instant, but I still hesitate to try new gourmet food categories.",
            "sentiment": "neutral",
            "barrier": "QUALITY_CONCERN"
        }
    ]
    save_raw_data(mock_reviews, "trustpilot")
    return mock_reviews

def fetch_gmb_reviews():
    """
    Simulates Google My Business location-based reviews.
    """
    mock_reviews = [
        {
            "id": "gmb_1",
            "source": "GMB",
            "content": "Dark store local stock for premium baby wipes is always low. I had to buy from another platform.",
            "sentiment": "negative",
            "barrier": "LIMITED_VARIETY"
        }
    ]
    save_raw_data(mock_reviews, "gmb")
    return mock_reviews

def fetch_glassdoor_feedback():
    """
    Simulates Glassdoor/AmbitionBox feedback.
    """
    mock_reviews = [
        {
            "id": "glassdoor_1",
            "source": "Glassdoor",
            "content": "Operations are fast, but catalog layout makes new category cross-selling hard to scale due to rigid tag management.",
            "sentiment": "neutral",
            "barrier": "HIDDEN_IN_UI"
        }
    ]
    save_raw_data(mock_reviews, "glassdoor")
    return mock_reviews
