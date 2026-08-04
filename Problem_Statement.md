# Problem Statement: Zepto AI-powered Discovery Engine

## Problem: Increasing Cross-Category Product Discovery on Zepto

Zepto has successfully become an integral part of users' weekly quick-commerce routines by enabling 10-minute delivery of groceries, snacks, beverages, and household essentials. While this convenience drives high repeat purchases and retention, it also reinforces **habitual shopping behavior**. Over time, most users repeatedly buy products from the same narrow set of categories and rarely explore the broader catalog available on the platform.

As a result, a significant portion of Monthly Active Customers (MACs) do not purchase from any new category during a given month. This limits opportunities for increased basket size, higher customer lifetime value (LTV), and broader product adoption across categories such as Gourmet Foods, Personal Care, Pet Supplies, and Baby Products.

### Strategic Examples of Target Category Transitions:
- **Groceries Buyer** $\rightarrow$ starts purchasing **Pet Supplies** or **Gourmet Produce**.
- **Snacks & Beverages Buyer** $\rightarrow$ starts purchasing **Personal Care & Wellness**.
- **Household Essentials Buyer** $\rightarrow$ starts purchasing **Baby Products & Toys**.

Current discovery mechanisms—such as keyword search, collaborative recommendations, banners, and category browsing—primarily optimize for relevance based on historical purchases. While effective for quick conversion, these systems create a **"habit loop"** that reinforces existing shopping patterns instead of encouraging catalog exploration.

To address this challenge, Zepto needs an AI-powered Discovery Engine that analyzes large-scale user feedback (specifically extracting reviews and discussions only about the Zepto App) across the following target sources:
- **Google Play Store**: https://play.google.com/store/apps/details?id=com.zeptoconsumerapp
- **Apple App Store**: https://apps.apple.com/in/app/zepto-10-minute-grocery/id1575323645
- **Reddit Discussions**: https://www.reddit.com/search/?q=Zepto
- **X (formerly Twitter)**: https://x.com/search
- **YouTube Reviews**: https://www.youtube.com/results?search_query=Zepto+review
- **Quora Discussions**: https://www.quora.com/search?q=Zepto
- **LinkedIn Articles**: https://www.linkedin.com/search/results/content/?keywords=quick%20commerce
- **Product Hunt**: https://www.producthunt.com/search?q=Zepto
- **Zendesk Ticket Logs**: Internal Customer Support logs and ticket queries
- **MouthShut Consumer Reviews**: https://www.mouthshut.com/product-reviews/Zepto-10-Minute-Grocery-Delivery-reviews-926105342
- **Trustpilot**: https://www.trustpilot.com/review/www.zeptonow.com
- **Google My Business (GMB)**: Location-specific dark store customer reviews
- **Glassdoor & AmbitionBox**: Internal employee feedback regarding checkout/catalog complaints

The system should identify why users stick to familiar categories, uncover barriers that prevent experimentation, understand how users currently discover products, and surface unmet needs and opportunities across different customer segments.

---

## 🎯 Strategic Goal

Increase the percentage of Monthly Active Customers who purchase products from **at least one new category every month** by using AI-driven customer insights to improve product discovery, personalization, and cross-category recommendations.

---

## 💡 Core PM Questions Answered by the AI Discovery Engine

The engine processes this data to answer:
1. **Why do users repeatedly buy from the same categories?** (Habit loop created by historic order optimization).
2. **What prevents users from exploring new categories?** (4 main barriers: `HIGH_PRICE`, `QUALITY_CONCERN`, `PACK_SIZE_TOO_LARGE`, `HIDDEN_IN_UI`).
3. **How do users discover products today?** (Search queries and immediate-need browsing).
4. **What role do habits play in shopping behavior?** (Quick <30s checkout loops on recurring items).
5. **What information do users need before trying a new category?** (Risk-reversing proof badges: farm-fresh guarantees, 200g trial packs).
6. **What frustrations emerge repeatedly?** (Hidden category UI, missing organic options, large minimum pack sizes).
7. **Which user segments are more likely to experiment?** (5 profiled cohorts: `Routine Buyers`, `Explorers`, `Deal Seekers`, `Families`, `Premium Users`).
8. **What unmet needs emerge consistently across discussions?** (Gluten-Free snacks, imported gourmet trial packs, eco-friendly cleaners).

---

## 📊 Success Metrics & KPIs

* **Discovery Rate (Primary):** % of Monthly Active Customers purchasing from at least one new category each month.
* **Cross-Category Conversion Rate:** Click-through and checkout rates from dynamic barrier-mitigating recommendation hooks (**+67.23% lift achieved in A/B testing**).
* **Average Order Value (AOV):** Increase in AOV through complementary category purchases (**+INR 115.32 boost per basket**).
* **Category Diversity:** Average unique categories purchased per customer per month.
* **Customer Retention & CSAT:** Maintaining high recommendation satisfaction while encouraging exploration.

---

## 🖥️ High-Fidelity Dashboard & Analytics Requirements (Growth PM Workspace)

The Zepto AI Discovery Engine features a premium desktop dashboard designed specifically for Zepto's Growth Product Team to analyze feedback, shopping behavior, and category transitions:

* **Top Navigation Bar**:
  * **Header Title**: `"AI-Powered Review Discovery Engine Dashboard"`
  * **Subtitle**: `"AI-powered Customer Insights & Category Growth Intelligence"`
  * **Controls**: Date range selector (dynamically updated to current client date with a calendar icon 📅 that is hidden in the exported report to keep print formatting clean), Notification icon, User profile, Export report button (active print window trigger).
* **Left Sidebar Navigation**:
  * Dashboard, Data Sources, AI Insights, Customer Behavior, User Segments, Category Opportunities, and Growth Actions (with A/B campaign triggers, REST API sandbox, and quality validation).
* **Overview Analytics Cards**:
  * **128K+** Customer Conversations Analyzed
  * **92%** AI Insight Confidence
  * **24** Emerging Customer Needs
  * **18** Categories Tracked
* **AI Feedback Intelligence Section**:
  * Large analytical panel connecting Play Store reviews, App Store reviews, Reddit discussions, Social Media, Forums, and Zendesk tickets. Shows sentiment graphs, positive vs negative volumes, and trending topics with interactive hover tooltips.
* **Customer Behavior Analytics**:
  * Visual representations (line charts, bar charts, heatmaps, funnel charts) of repeat purchase behavior, category buying patterns, and new category adoption rates, including a 90-day sentiment area tracker and interactive hover tooltips.
* **Dynamic AI Insight Cards**:
  * *"Users repeat grocery purchases because reordering is faster than exploring."*
  * *"Customers need reviews and trust signals before trying new categories."*
  * *"Personal Care has high cross-category potential among grocery buyers."*
* **User Segmentation Panel**:
  * Cohort profiles for **Routine Buyers**, **Explorers**, **Deal Seekers**, **Families**, and **Premium Users** (tracking size, behavior, exploration probability, and category preference).
* **Growth Opportunity Engine**:
  * Actionable category transitions: Grocery $\rightarrow$ Personal Care, Snacks $\rightarrow$ Beverages, and Household $\rightarrow$ Baby Care.
* **UI Design Direction**: Glowing Dark Glassmorphism workspace theme (deep purple/blue backgrounds, cyan/mint accents, electric pink highlights) with rounded cards, glowing soft shadows, translucent glassmorphic panels, and enhanced typography legibility (featuring 16px quote font-sizes and 13px friction/affinity badge tag sizing with 4px 8px padding).
* **Production Scheduler & Drift Monitoring**:
  * Automated background daemon scheduling ingestion and processing runs at exactly **10:00 AM IST daily**.
  * Auto-validation checks verifying schema compliance, cleaning PII, and raising alerts on model response anomalies.

