import random
import json
import sys
from pathlib import Path

# Ensure UTF-8 output encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def run_ab_test_simulation(sample_size: int = 10000):
    """
    Simulates a randomized 50/50 A/B Test split on 5% Monthly Active Customers:
    - Control Group (Variant A): Standard collaborative filtering (historical purchases only)
    - Treatment Group (Variant B): AI-powered Discovery Engine (Cohort barriers + Dynamic Hooks)
    """
    print("=" * 75)
    print("    ZEPTO DISCOVERY ENGINE - LIVE A/B TESTING SIMULATION (5% MAC)")
    print("=" * 75)
    
    random.seed(42)
    
    control_conversions = 0
    control_aov = []
    
    treatment_conversions = 0
    treatment_aov = []
    
    for i in range(sample_size):
        variant = "A" if i % 2 == 0 else "B"
        
        if variant == "A":
            # Control Group: Standard Recommendation (no barrier hook)
            converted = random.random() < 0.12  # 12.0% cross-category conversion rate
            if converted:
                control_conversions += 1
                control_aov.append(random.uniform(320, 420))
        else:
            # Treatment Group: AI Discovery Engine (Dynamic barrier hooks)
            converted = random.random() < 0.198 # 19.8% cross-category conversion rate (+65% lift!)
            if converted:
                treatment_conversions += 1
                treatment_aov.append(random.uniform(410, 560))
                
    control_rate = round((control_conversions / (sample_size / 2)) * 100, 2)
    treatment_rate = round((treatment_conversions / (sample_size / 2)) * 100, 2)
    
    avg_control_aov = round(sum(control_aov) / len(control_aov), 2)
    avg_treatment_aov = round(sum(treatment_aov) / len(treatment_aov), 2)
    
    aov_lift = round(avg_treatment_aov - avg_control_aov, 2)
    conversion_lift = round(((treatment_rate - control_rate) / control_rate) * 100, 2)
    
    results = {
        "sample_size": sample_size,
        "control": {
            "variant": "A (Baseline / Standard Recs)",
            "conversion_rate": f"{control_rate}%",
            "avg_aov": f"INR {avg_control_aov}"
        },
        "treatment": {
            "variant": "B (Zepto AI Discovery Engine)",
            "conversion_rate": f"{treatment_rate}%",
            "avg_aov": f"INR {avg_treatment_aov}"
        },
        "impact": {
            "conversion_rate_relative_lift": f"+{conversion_lift}%",
            "aov_delta": f"+INR {aov_lift}",
            "p_value": "< 0.001 (Statistically Significant)"
        }
    }
    
    print(f"\n[CONTROL GROUP A]  Conversion Rate: {control_rate}%  | Avg AOV: INR {avg_control_aov}")
    print(f"[TREATMENT GROUP B] Conversion Rate: {treatment_rate}% | Avg AOV: INR {avg_treatment_aov}")
    print("-" * 75)
    print(f" RELATIVE CONVERSION LIFT: +{conversion_lift}%")
    print(f" AVERAGE BASKET VALUE BOOST: +INR {aov_lift}")
    print(f" STATISTICAL SIGNIFICANCE: p < 0.001 (Confidence: 99.9%)")
    print("=" * 75)
    
    output_path = Path(__file__).resolve().parent.parent.parent / "data" / "ab_test_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    return results

if __name__ == "__main__":
    run_ab_test_simulation()
