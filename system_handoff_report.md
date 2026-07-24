# System Hand-Off Report & Model Drift Monitoring

This document details the production hand-off procedures, architecture maintenance guidelines, and model drift monitoring pipeline for the **Zepto AI-powered Discovery Engine**.

---

## 🏗️ Production Architecture Summary

```
[External Sources] -> [Phase 1 Ingestion] -> [Phase 2 Groq LLM] -> [Phase 3 Cohorts Dashboard] -> [Phase 4 Personalization API]
 (App Stores/Reddit)     (Airflow/S3)         (ABSA / Vector DB)      (Retool / Glass UI)          (Feast Feature Store)
```

- **Ingestion Microservices (`src/ingestion/`)**: Automated DAGs pulling App Store, Play Store, Reddit, Zendesk, and Social Media mentions.
- **AI Processing Pipeline (`src/processing/`)**: Groq LPU inference (`llama-3.3-70b-versatile`) performing ABSA and barrier classification.
- **Analytics & Dashboard (`src/analytics/` & `dashboard/`)**: Glassmorphism UI serving real-time cohort distributions.
- **Personalization REST API (`src/personalization/`)**: Low-latency REST API (`/v1/user/discovery-recommendations`) serving dynamic hooks.

---

## 📈 Model Drift & Health Monitoring

To maintain model accuracy and operational health in production:

1. **Groq LLM Output Quality Monitoring**:
   - Automated weekly evaluation of JSON parsing error rates (alert threshold $> 1\%$).
   - Periodic review of ABSA precision against human-annotated sample batches.

2. **Data Pipeline Drift Alerts**:
   - Monitor review volume anomalies (e.g., sudden drop in Play Store ingestion triggers PagerDuty alert).
   - Re-cluster customer cohorts monthly in Snowflake to detect emerging purchase barriers.

3. **Latency & SLA Capping**:
   - Downstream Personalization API latency must remain $< 5\text{ms}$ at p99.
