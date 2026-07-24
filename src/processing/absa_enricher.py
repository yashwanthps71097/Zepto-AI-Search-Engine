from src.processing.preprocessor import clean_text
from src.processing.groq_client import analyze_review_with_groq

def enrich_review_record(record: dict) -> dict:
    """
    Cleans raw review text and enriches it with ABSA sentiment and barrier tags via Groq LLM.
    """
    raw_content = record.get("content") or record.get("description") or record.get("title") or ""
    cleaned_content = clean_text(raw_content)
    
    if not cleaned_content:
        ai_insights = {
            "sentiment": "NEUTRAL",
            "target_category": None,
            "aspects": [],
            "purchase_barrier": None,
            "unmet_need": None,
            "summary": "Empty or non-text review"
        }
    else:
        ai_insights = analyze_review_with_groq(cleaned_content)
        
    enriched_record = {
        **record,
        "cleaned_content": cleaned_content,
        "ai_enrichment": ai_insights
    }
    
    return enriched_record
