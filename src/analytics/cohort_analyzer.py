import json
from pathlib import Path

ENRICHED_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "enriched" / "zepto_enriched_insights.json"
ANALYTICS_OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "analytics_summary.json"

def analyze_cohorts_and_barriers():
    """
    Analyzes enriched review data to generate segment breakdowns, top category friction points,
    and trending unmet customer needs for the premium white SaaS Discovery Dashboard.
    Profiles 5 segments: Routine Buyers, Explorers, Deal Seekers, Families, Premium Users.
    """
    if not ENRICHED_DATA_PATH.exists():
        print("[ANALYTICS ERROR] Enriched insights file not found. Run Phase 2 first!")
        return {}

    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    total_records = len(records)
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    barrier_counts = {}
    category_barriers = {}
    unmet_needs = []
    
    # 5 Target Customer Segments
    cohorts = {
        "Routine Buyers": 0,
        "Explorers": 0,
        "Deal Seekers": 0,
        "Families": 0,
        "Premium Users": 0
    }

    for record in records:
        ai_data = record.get("ai_enrichment", {})
        sentiment = ai_data.get("sentiment", "NEUTRAL")
        barrier = ai_data.get("purchase_barrier")
        category = ai_data.get("target_category") or "General"
        unmet = ai_data.get("unmet_need")

        # Sentiment counter
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1

        # Barrier counter
        if barrier:
            barrier_counts[barrier] = barrier_counts.get(barrier, 0) + 1
            if category not in category_barriers:
                category_barriers[category] = []
            category_barriers[category].append(barrier)

        # Mapping logic for 5 Growth Segments based on data attributes
        content = record.get("content", "").lower()
        if any(kw in content for kw in ["organic", "gourmet", "premium", "brand", "quality"]):
            cohorts["Premium Users"] += 1
        elif any(kw in content for kw in ["baby", "kid", "diaper", "wipes", "child"]):
            cohorts["Families"] += 1
        elif any(kw in content for kw in ["price", "discount", "coupon", "cheap", "expensive", "trial"]):
            cohorts["Deal Seekers"] += 1
        elif any(kw in content for kw in ["habit", "routine", "every day", "milk", "daily", "fast", "repeat"]):
            cohorts["Routine Buyers"] += 1
        else:
            cohorts["Explorers"] += 1

        if unmet:
            unmet_needs.append({
                "source": record.get("source"),
                "text": unmet,
                "category": category
            })

    summary = {
        "total_analyzed": total_records,
        "sentiment_breakdown": sentiment_counts,
        "top_barriers": barrier_counts,
        "category_barriers": category_barriers,
        "cohort_segments": cohorts,
        "unmet_needs_feed": unmet_needs
    }

    ANALYTICS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ANALYTICS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[ANALYTICS SUCCESS] Generated analytics summary at {ANALYTICS_OUTPUT_PATH}")
    return summary

if __name__ == "__main__":
    analyze_cohorts_and_barriers()
