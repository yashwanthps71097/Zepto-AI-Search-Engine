import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

def get_groq_client():
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("your_"):
        raise ValueError("GROQ_API_KEY is missing or invalid in .env file.")
    return Groq(api_key=GROQ_API_KEY)

def analyze_review_with_groq(review_text: str, model: str = "llama-3.3-70b-versatile") -> dict:
    """
    Sends review text to Groq LPU inference API to perform Aspect-Based Sentiment Analysis (ABSA)
    and extract category discovery barriers. Returns structured JSON output.
    """
    system_prompt = """
    You are an expert AI Analyst for Zepto's Product & Growth team.
    Analyze the given customer review about the Zepto App and extract structured JSON with the following keys:
    - "sentiment": "POSITIVE", "NEGATIVE", or "NEUTRAL"
    - "target_category": string or null (e.g., "Produce", "Snacks", "Gourmet", "Household", "Dairy")
    - "aspects": list of strings (e.g., ["price", "delivery_speed", "item_quality", "search_discovery", "pack_size"])
    - "purchase_barrier": string or null (e.g., "HIGH_PRICE", "HIDDEN_IN_UI", "PACK_SIZE_TOO_LARGE", "QUALITY_CONCERN", "LIMITED_VARIETY")
    - "unmet_need": string or null (brief description of any product request)
    - "summary": concise 1-sentence summary of customer feedback

    Respond ONLY in raw valid JSON format without markdown code blocks.
    """

    user_prompt = f"Customer Review Text: \"{review_text}\""

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"[GROQ ERROR] LLM analysis failed: {e}")
        # Rule-based fallback if API key rate-limited or unavailable
        return fallback_rule_based_analysis(review_text)

def fallback_rule_based_analysis(text: str) -> dict:
    text_lower = text.lower()
    barrier = None
    category = None
    
    if "expensive" in text_lower or "price" in text_lower or "cost" in text_lower:
        barrier = "HIGH_PRICE"
    elif "wrong" in text_lower or "missing" in text_lower or "quality" in text_lower:
        barrier = "QUALITY_CONCERN"
    elif "hidden" in text_lower or "search" in text_lower or "find" in text_lower:
        barrier = "HIDDEN_IN_UI"

    if "fruit" in text_lower or "vegetable" in text_lower or "apple" in text_lower:
        category = "Produce"
    elif "snack" in text_lower or "chip" in text_lower or "drink" in text_lower:
        category = "Snacks"

    return {
        "sentiment": "NEGATIVE" if ("wrong" in text_lower or "missing" in text_lower or "expensive" in text_lower) else "POSITIVE",
        "target_category": category,
        "aspects": ["delivery_quality"] if "missing" in text_lower else ["pricing"],
        "purchase_barrier": barrier,
        "unmet_need": text if "missing" in text_lower else None,
        "summary": text[:100]
    }
