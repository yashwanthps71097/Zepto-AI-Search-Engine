import os
import requests
from dotenv import load_dotenv
from src.ingestion.storage import save_raw_data

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN", "zepto")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL", "")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN", "")

def fetch_zendesk_support_tickets():
    """
    Fetches customer support logs from Zendesk API regarding Zepto App feedback.
    Falls back to synthetic/mock support sample data if credentials are placeholders.
    """
    print("[ZENDESK] Fetching customer support ticket logs for Zepto App...")
    
    if ZENDESK_API_TOKEN and ZENDESK_API_TOKEN != "your_zendesk_api_token":
        url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json"
        auth = (f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)
        try:
            response = requests.get(url, auth=auth, timeout=10)
            response.raise_for_status()
            tickets = response.json().get("tickets", [])
            formatted = []
            for t in tickets:
                formatted.append({
                    "source": "zendesk",
                    "app_name": "Zepto",
                    "ticket_id": t.get("id"),
                    "subject": t.get("subject"),
                    "description": t.get("description"),
                    "category": t.get("type"),
                    "created_at": t.get("created_at")
                })
            save_raw_data(formatted, "zendesk")
            return formatted
        except Exception as e:
            print(f"[ZENDESK WARNING] Could not fetch live tickets: {e}. Generating sample ingestion schema.")
    
    # Mock/Sample schema for demonstration when API token is placeholder
    mock_tickets = [
        {
            "source": "zendesk",
            "app_name": "Zepto",
            "ticket_id": 10001,
            "subject": "Cannot find organic fruits in search",
            "description": "I tried searching for organic apples on the Zepto app, but only standard apples show up. Is there an organic category?",
            "category": "search_issue",
            "created_at": "2026-07-20T10:15:00Z"
        },
        {
            "source": "zendesk",
            "app_name": "Zepto",
            "ticket_id": 10002,
            "subject": "High price for gourmet cheese",
            "description": "I wanted to try imported cheese from the gourmet section, but the minimum pack size is 500g which is too big and expensive for trial.",
            "category": "pricing_pack_size",
            "created_at": "2026-07-20T11:42:00Z"
        }
    ]
    save_raw_data(mock_tickets, "zendesk")
    return mock_tickets

if __name__ == "__main__":
    fetch_zendesk_support_tickets()
