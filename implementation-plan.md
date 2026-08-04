# Phase-Wise Implementation Roadmap: Zepto AI-powered Discovery Engine

This document outlines the complete implementation roadmap and phase-wise deliverables for building, deploying, and evaluating the **Zepto AI-powered Discovery Engine**.

---

## 📅 Roadmap Overview

```
                      ┌─────────────────────────────────────────┐
                      │  Phase 1: Multi-Channel Ingestion (W1-3)│
                      └────────────────────┬────────────────────┘
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  Phase 2: Groq LLM Processing (W4-W7)  │
                      └────────────────────┬────────────────────┘
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  Phase 3: Dashboard & Cohorts (W8-W10)  │
                      └────────────────────┬────────────────────┘
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  Phase 4: Personalization REST API (W11)│
                      └────────────────────┬────────────────────┘
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  Phase 5: A/B Testing & Hand-off (W14) │
                      └─────────────────────────────────────────┘
```

---

## 🛠️ Phase Detail

### Phase 1: Ingestion & Storage Setup (Weeks 1 - 3)
**Objective:** Connect to all external feedback sources and internal ticket databases to extract reviews specifically targeting the **Zepto App**.

* **Tasks:**
  * Configure Google Play Store connector for package `com.zeptoconsumerapp` (https://play.google.com/store/apps/details?id=com.zeptoconsumerapp).
  * Configure Apple App Store connector for Zepto App ID `1582236968` (https://apps.apple.com/in/app/zepto-10-minute-grocery/id1575323645).
  * Build Reddit API / PRAW connector to search discussions regarding Zepto (https://www.reddit.com/search/?q=Zepto).
  * Build X / Twitter search API collector (https://x.com/search).
  * Build collectors for YouTube reviews, Quora discussions, LinkedIn articles, and Product Hunt.
  * Ingest Zendesk ticket logs, MouthShut consumer reviews, Trustpilot reviews, GMB location reviews, and employee feedback (Glassdoor/AmbitionBox).
* **Deliverables:**
  * Executable ingestion pipeline (`python -m src.ingestion.main_ingestion`).
  * Raw dataset saved to `data/raw/`.

---

### Phase 2: AI Processing Pipeline & Groq LLM Enrichment (Weeks 4 - 7)
**Objective:** Build the NLP pipeline to scrub PII, extract Aspect-Based Sentiment Analysis (ABSA), and classify purchase barriers using Groq's high-speed LPU LLMs.

* **Tasks:**
  * Build PII scrubbing & text preprocessor (`src/processing/preprocessor.py`).
  * Integrate **Groq API Client (`src/processing/groq_client.py`)** using model `llama-3.3-70b-versatile` with structured JSON mode.
  * Classify 4 purchase barriers (`HIGH_PRICE`, `QUALITY_CONCERN`, `PACK_SIZE_TOO_LARGE`, `HIDDEN_IN_UI`).
  * Format vector index payloads for Pinecone (`src/processing/vector_indexer.py`).
* **Deliverables:**
  * Executable AI enrichment pipeline (`python -m src.processing.main_processing`).
  * Enriched JSON insights dataset saved at `data/enriched/zepto_enriched_insights.json`.

---

### Phase 3: Cohort Profiling & Analytics Dashboard (Weeks 8 - 10)
**Objective:** Cluster feedback attributes into customer growth cohorts and build an interactive premium glowing dark glassmorphic dashboard UI for the Growth team.

* **Tasks:**
  * Build cohort analyzer microservice (`src/analytics/cohort_analyzer.py`) profiling 5 segments (`Routine Buyers`, `Explorers`, `Deal Seekers`, `Families`, `Premium Users`).
  * Build premium glowing dark glassmorphism **AI-Powered Review Discovery Engine Dashboard (`dashboard/index.html`, `styles.css`, `app.js`)** featuring:
    * Left sidebar navigation (Dashboard, Data Sources, AI Insights, Customer Behavior, User Segments, Category Opportunities, Growth Actions).
    * Overview cards tracking 128K+ conversations, 92% confidence score, 24 emerging needs, and 18 categories.
    * Interactive feedback intelligence panels, visual line/bar/heatmap charts, dynamic AI insight cards, a 90-day sentiment area wave tracker, and hover tooltips on all segments.
    * High-legibility typography improvements (16px audit log quotes, 13px friction tags and affinity badges with 4px 8px padding).
    * Date Display styling: Includes a calendar date icon (📅) before the date badge in the web application UI, which is dynamically hidden in the exported PDF report.
* **Deliverables:**
  * Live premium web dashboard served at `http://localhost:8080`.
  * Analytics summary dataset saved at `data/analytics_summary.json`.

---

### Phase 4: Downstream Personalization Integration (Weeks 11 - 13)
**Objective:** Link discovery engine insights to Zepto's live catalog via Feast Feature Store and low-latency REST API endpoints.

* **Tasks:**
  * Implement **Feast Feature Store Mock (`src/personalization/feature_store.py`)** serving user feature vectors at $< 2\text{ms}$ latency.
  * Implement **Dynamic Hook Generator (`src/personalization/hook_generator.py`)** generating risk-reversing badge copy.
  * Implement **Personalization REST API (`src/personalization/recommendation_api.py`)** serving `/v1/user/discovery-recommendations`.
* **Deliverables:**
  * Live REST API server running on `http://localhost:8081`.

---

### Phase 5: A/B Testing & Optimization (Weeks 14 - 16)
**Objective:** Conduct offline metric evaluations and a randomized 50/50 A/B test simulation across 5% of Monthly Active Customers (MACs).

* **Tasks:**
  * Build offline evaluator (`src/evaluation/evaluator.py`) measuring Precision@3 (33.3%) and Catalog Diversity (0.29).
  * Build A/B test simulator (`src/evaluation/ab_testing_framework.py`) demonstrating a **+67.23% relative conversion lift** and **+INR 115.32 AOV boost**.
* **Deliverables:**
  * A/B Test Results Report ([ab_test_results.md](file:///c:/Users/ADMIN/Desktop/Product%20Owner/Graduation%20Project/ab_test_results.md)).
  * System Hand-Off Report ([system_handoff_report.md](file:///c:/Users/ADMIN/Desktop/Product%20Owner/Graduation%20Project/system_handoff_report.md)).

---

### Phase 6: Automated Daily Scheduler Daemon (Weeks 17 - 18)
**Objective:** Implement an automated local daemon to execute the ingestion and Groq AI enrichment pipeline daily at exactly 10:00 AM IST.

* **Tasks:**
  * Build timezone-aware production scheduler (`run_scheduler.py`) supporting IST (UTC+5:30) timezone calculation.
  * Implement sleep and execution handlers running the pipeline sequentially.
* **Deliverables:**
  * Running Scheduler Daemon (`run_scheduler.py`).

---

### Phase 7: Model Drift & Quality Monitoring (Weeks 19 - 20)
**Objective:** Set up automated format verification and sentiment distribution drift monitoring for LLM operations.

* **Tasks:**
  * Build automated compliance script (`src/evaluation/drift_monitor.py`) verifying schema, scrubbing PII, and logging alerts.
  * Generate diagnostic report detailing system status (HEALTHY, DEGRADED, DRIFT_ALERT).
* **Deliverables:**
  * Automated Quality Validation Script ([drift_monitor.py](file:///c:/Users/ADMIN/Desktop/Product%20Owner/Graduation%20Project/src/evaluation/drift_monitor.py)).
  * Drift Monitor Summary Dataset (`data/drift_monitor_report.json`).

