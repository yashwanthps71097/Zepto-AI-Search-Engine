import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.ingestion.google_play import fetch_google_play_reviews
from src.ingestion.app_store import fetch_app_store_reviews
from src.ingestion.reddit import fetch_reddit_zepto_discussions
from src.ingestion.social_media import fetch_social_media_mentions
from src.ingestion.zendesk import fetch_zendesk_support_tickets
from src.ingestion.other_sources import (
    fetch_youtube_reviews,
    fetch_quora_discussions,
    fetch_linkedin_articles,
    fetch_product_hunt_feedback,
    fetch_mouthshut_reviews,
    fetch_trustpilot_reviews,
    fetch_gmb_reviews,
    fetch_glassdoor_feedback
)

def run_phase_1_ingestion():
    """
    Orchestrates Phase 1: Ingestion of Zepto App reviews and discussions
    across Google Play Store, Apple App Store, Reddit, Social Media, Zendesk,
    YouTube, Quora, LinkedIn, Product Hunt, MouthShut, Trustpilot, GMB, and Glassdoor.
    """
    print("=" * 75)
    print("      ZEPTO DISCOVERY ENGINE - PHASE 1 INGESTION PIPELINE")
    print("=" * 75)
    
    # 1. Google Play Store Reviews
    print("\n---> [1/13] Running Google Play Store Reviews Collector...")
    gp_data = fetch_google_play_reviews(count=100)
    
    # 2. Apple App Store Reviews
    print("\n---> [2/13] Running Apple App Store Reviews Collector...")
    as_data = fetch_app_store_reviews()
    
    # 3. Reddit Discussions
    print("\n---> [3/13] Running Reddit Discussions Collector...")
    reddit_data = fetch_reddit_zepto_discussions(limit=50)

    # 4. Social Media Conversations
    print("\n---> [4/13] Running Social Media Collector...")
    social_data = fetch_social_media_mentions()
    
    # 5. Zendesk Customer Support Tickets
    print("\n---> [5/13] Running Zendesk Support Tickets Collector...")
    zendesk_data = fetch_zendesk_support_tickets()
    
    # 6. YouTube Video Reviews
    print("\n---> [6/13] Running YouTube Reviews Collector...")
    yt_data = fetch_youtube_reviews()

    # 7. Quora Discussions
    print("\n---> [7/13] Running Quora Discussions Collector...")
    quora_data = fetch_quora_discussions()

    # 8. LinkedIn Articles
    print("\n---> [8/13] Running LinkedIn Articles Collector...")
    li_data = fetch_linkedin_articles()

    # 9. Product Hunt Feedback
    print("\n---> [9/13] Running Product Hunt Feedback Collector...")
    ph_data = fetch_product_hunt_feedback()

    # 10. MouthShut Reviews
    print("\n---> [10/13] Running MouthShut Reviews Collector...")
    ms_data = fetch_mouthshut_reviews()

    # 11. Trustpilot Reviews
    print("\n---> [11/13] Running Trustpilot Reviews Collector...")
    tp_data = fetch_trustpilot_reviews()

    # 12. GMB Reviews
    print("\n---> [12/13] Running GMB Reviews Collector...")
    gmb_data = fetch_gmb_reviews()

    # 13. Glassdoor Employee Feedback
    print("\n---> [13/13] Running Glassdoor Employee Feedback Collector...")
    gd_data = fetch_glassdoor_feedback()

    total_records = (
        len(gp_data) + len(as_data) + len(reddit_data) + len(social_data) + len(zendesk_data) +
        len(yt_data) + len(quora_data) + len(li_data) + len(ph_data) + len(ms_data) +
        len(tp_data) + len(gmb_data) + len(gd_data)
    )
    
    print("\n" + "=" * 75)
    print(f" Phase 1 Ingestion Complete!")
    print(f" Total Zepto App Review/Feedback Records Ingested: {total_records}")
    print(f" Landing Location: data/raw/")
    print("=" * 75)

if __name__ == "__main__":
    run_phase_1_ingestion()
