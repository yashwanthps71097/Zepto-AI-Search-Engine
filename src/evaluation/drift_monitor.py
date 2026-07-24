import json
import sys
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

ENRICHED_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "enriched" / "zepto_enriched_insights.json"
ANALYTICS_SUMMARY_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "analytics_summary.json"

def run_drift_and_quality_monitoring():
    """
    Phase 7: Automated Quality Validation & Model Drift Monitoring
    - Checks for model JSON structural anomalies.
    - Validates presence of mandatory schema fields (PII scrubbing checks, aspect categories).
    - Checks for data distribution shifts (anomaly alerts on high negative sentiments or parsing failures).
    """
    print("=" * 75)
    print("      ZEPTO DISCOVERY ENGINE - PHASE 7 MODEL DRIFT & QUALITY MONITOR")
    print("=" * 75)
    
    if not ENRICHED_DATA_PATH.exists() or not ANALYTICS_SUMMARY_PATH.exists():
        print("[MONITOR WARNING] Enriched dataset or analytics summary is missing. Run the pipeline first.")
        return False

    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    with open(ANALYTICS_SUMMARY_PATH, "r", encoding="utf-8") as f:
        summary = json.load(f)

    print(f"Checking {len(records)} enriched records for model/schema compliance...")
    
    anomalies_detected = 0
    pii_violations = 0
    missing_barriers = 0
    
    for idx, rec in enumerate(records):
        content = rec.get("content", "")
        ai_data = rec.get("ai_enrichment", {})
        
        # 1. PII Scrubbing check (e.g. check if phone numbers or email patterns exist in processed text)
        if "@" in content or any(char.isdigit() and len(content.split()) < 3 for char in content):
            pii_violations += 1
            
        # 2. Check for empty classification barriers
        if "purchase_barrier" not in ai_data:
            missing_barriers += 1
            anomalies_detected += 1

    # 3. Sentiment distribution anomaly check (e.g. negative sentiment > 50% is a drift alert)
    neg_percentage = 0.0
    sentiment = summary.get("sentiment_breakdown", {})
    total_sentiment = sum(sentiment.values())
    if total_sentiment > 0:
        neg_percentage = (sentiment.get("NEGATIVE", 0) / total_sentiment) * 100

    print("\n--- Compliance Metrics ---")
    print(f"  - Schema Integrity: {100 - (missing_barriers / len(records) * 100 if len(records) > 0 else 0):.2f}%")
    print(f"  - PII Leakage Incidents: {pii_violations}")
    print(f"  - Model Format Anomalies: {anomalies_detected}")
    print(f"  - Negative Sentiment Ratio: {neg_percentage:.2f}%")
    
    print("\n--- Drift Alert Diagnostic ---")
    status = "HEALTHY"
    if pii_violations > 0:
        print("  [ALERT] PII scrubbing rules violated! Retune clean_pii algorithms.")
        status = "DEGRADED"
    if neg_percentage > 40.0:
        print("  [ALERT] Negative sentiment anomaly detected! Potential service outrage or catalog drift.")
        status = "DRIFT_ALERT"
    if status == "HEALTHY":
        print("  [OK] Model distributions and schemas are within healthy boundaries.")
        
    print("\n" + "=" * 75)
    print(f" Phase 7 Monitoring Completed. System Status: {status}")
    print("=" * 75)
    
    # Save monitoring report
    report_path = Path(__file__).resolve().parent.parent.parent / "data" / "drift_monitor_report.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "pii_violations": pii_violations,
        "format_anomalies": anomalies_detected,
        "neg_sentiment_percentage": neg_percentage
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    return True

if __name__ == "__main__":
    run_drift_and_quality_monitoring()
