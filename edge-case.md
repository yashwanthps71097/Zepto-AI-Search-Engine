# Edge-Case Handling Strategy: Zepto AI-powered Discovery Engine

This document details all potential edge cases across the **Zepto AI-powered Discovery Engine** pipeline and defines the handling strategies, fallback mechanisms, and validation rules for each.

---

## 1. 📥 Data Ingestion & Data Quality Edge Cases

| Category | Edge Case Scenario | Potential Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Non-Text / Emoji Reviews** | Customer submits reviews containing only emojis (e.g., `🥰`, `👎👎👎`). | LLM analysis failure or empty string input error. | Preprocessor detects emoji-only input, converts common emojis to text tokens (e.g., `👎` $\rightarrow$ `negative_sentiment`), or routes directly to heuristic rating-based sentiment without calling LLM. |
| **Multilingual & Hinglish** | Feedback written in Hinglish or regional Indian languages (e.g., *"zepto me organic milk nahi mil raha"*). | Standard English tokenizers miss category intent. | Groq LPU models (Llama 3.3 / Mixtral) natively handle Hinglish context. Text preprocessor adds language detection tag `lang: hi-en` to guide prompt context. |
| **Spam & Duplicate Feedback** | Bots or automated scripts posting identical reviews multiple times. | Skews barrier metrics and wastes LLM API tokens. | Exact and fuzzy hash deduplication (MinHash / MD5 on cleaned text) before pushing to AI enrichment pipeline. |
| **Extremely Long Text** | Customer submits a 3,000-word detailed complaint log. | Exceeds context window or spikes token costs. | Truncate raw review text to the first 1,500 characters while preserving initial sentiment-heavy clauses. |
| **API Rate Limits / Outages** | App Store / Play Store / Reddit APIs return `429 Too Many Requests` or `403 Forbidden`. | Pipeline execution halts midway. | Exponential backoff retries with jitter; automatic fallback to cached proxy endpoints and alert triggers for tech ops. |

---

## 2. 🤖 AI Processing & Groq LLM Edge Cases

| Category | Edge Case Scenario | Potential Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Groq API Rate Limiting** | Exceeding Tokens Per Minute (TPM) or Requests Per Minute (RPM) during peak batch ingestion. | AI enrichment job failures. | Implement Redis/Celery queue batching. If Groq returns 429, retry after headers `Retry-After` delay. Fall back to local rule-based heuristic classifier (`fallback_rule_based_analysis`). |
| **Malformed JSON Response** | LLM outputs non-JSON text or broken JSON syntax despite `json_object` mode request. | JSON parsing error crashes pipeline. | Wrap LLM parser in `try...except json.JSONDecodeError`. Run regex JSON repair or re-query with deterministic temperature `0.0`. |
| **Sarcasm Detection** | Review uses sarcastic language (e.g., *"Great job delivering broken eggs in 10 mins! Very helpful."*). | Misclassified as `POSITIVE` sentiment. | LLM prompt explicitly instructs ABSA engine to cross-check text tone against numerical rating (e.g., 1-star rating with "Great job" indicates sarcasm $\rightarrow$ `NEGATIVE`). |
| **Competitor Mentions** | Review mentions rival apps (e.g., *"Blinkit has better discounts on gourmet cheese"*). | Confusion on app target. | Extractor tags competitor mentions into `competitor_benchmark` metadata field rather than flagging as internal Zepto app bug. |
| **Multi-Topic / Conflicting Feedback** | Single review contains mixed signals (e.g., *"Super fast delivery, but organic vegetables were stale and costly"*). | Single sentiment tag is inaccurate. | Aspect-Based Sentiment Analysis (ABSA) breaks feedback into itemized aspect-sentiment pairs: `delivery_speed: POSITIVE`, `produce_quality: NEGATIVE`, `price: NEGATIVE`. |

---

## 3. 💾 Data Storage & Vector Database Edge Cases

| Category | Edge Case Scenario | Potential Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Duplicate Vector IDs** | Re-ingesting reviews creates duplicate vector IDs in Pinecone. | Index corruption or inflated cluster counts. | Deterministic vector ID generation format: `vec_<source>_<review_id>`. Pinecone automatically upserts existing IDs instead of creating duplicates. |
| **Vector DB Downtime** | Pinecone / Vector DB connection timeout during indexing. | Vector loss for enriched reviews. | Buffer vector payloads locally in `data/enriched/` JSON files before pushing; retry batch indexing upon service recovery. |

---

## 4. 🎯 Personalization & Downstream UI Edge Cases

| Category | Edge Case Scenario | Potential Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Cold-Start User** | New Monthly Active Customer with zero purchase history. | Cannot determine habit loop or category barriers. | Recommend globally popular cross-category starter bundles (e.g., "Top-Rated Fresh Produce") until 3 orders are placed. |
| **Out-of-Stock Recommendation** | Personalization engine recommends a new category item that is out of stock in the user's micro-warehouse. | Severe user frustration & bounce. | Real-time stock filter query against local dark-store inventory before serving dynamic hooks or recommendations. |
| **Recommendation Fatigue** | Showing the same cross-category promo banner repeatedly to a user who repeatedly ignores it. | User ignores banners (banner blindness). | Cap frequency to 3 impressions per category per week. Rotate target categories if user does not convert. |
