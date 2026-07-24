import json
from pathlib import Path

ANALYTICS_SUMMARY_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "analytics_summary.json"

class FeastFeatureStoreMock:
    """
    Feast Feature Store client interface serving user affinity vectors,
    category barriers, and cohort profiles at ultra-low latency (<5ms).
    """
    def __init__(self):
        self.user_features = {
            "usr_1001": {
                "cohort": "Quality-Conscious Skeptics",
                "affinity_category": "Produce",
                "top_barrier": "QUALITY_CONCERN",
                "habitual_category": "Snacks"
            },
            "usr_1002": {
                "cohort": "Budget-Bound Planners",
                "affinity_category": "Gourmet",
                "top_barrier": "HIGH_PRICE",
                "habitual_category": "Dairy"
            },
            "usr_1003": {
                "cohort": "UI & Discovery Seekers",
                "affinity_category": "Household",
                "top_barrier": "HIDDEN_IN_UI",
                "habitual_category": "Beverages"
            }
        }

    def get_user_features(self, user_id: str) -> dict:
        """
        Retrieves low-latency feature vector for a specific user ID.
        """
        return self.user_features.get(user_id, {
            "cohort": "Convenience Loyalists",
            "affinity_category": "Produce",
            "top_barrier": None,
            "habitual_category": "General"
        })

feature_store = FeastFeatureStoreMock()
