import math

def calculate_precision_at_k(actual: list, recommended: list, k: int = 3) -> float:
    """Calculates Precision@K metric for recommendations."""
    recommended_at_k = recommended[:k]
    hits = sum(1 for item in recommended_at_k if item in actual)
    return round(hits / k, 4)

def calculate_catalog_diversity(recommended_categories: list, total_categories: int = 8) -> float:
    """Calculates Entropy-based Category Diversity Score."""
    if not recommended_categories:
        return 0.0
    unique_cats = set(recommended_categories)
    return round(len(unique_cats) / total_categories, 4)

def run_offline_evaluation():
    """
    Evaluates offline recommendation performance for the Zepto Discovery Engine.
    """
    print("=" * 75)
    print("      ZEPTO DISCOVERY ENGINE - OFFLINE EVALUATION METRICS")
    print("=" * 75)
    
    # Ground truth vs recommended discovery items
    test_cases = [
        {"user": "usr_1001", "purchased": ["Organic Farm Fresh Apples"], "recommended": ["Organic Farm Fresh Apples", "Gourmet Aged Cheddar", "Bamboo Cleaners"], "cats": ["Produce", "Gourmet", "Household"]},
        {"user": "usr_1002", "purchased": ["Gourmet Aged Cheddar"], "recommended": ["Gourmet Aged Cheddar", "Almond Flour"], "cats": ["Gourmet", "Produce"]},
        {"user": "usr_1003", "purchased": ["Eco-Friendly Bamboo Cleaners"], "recommended": ["Eco-Friendly Bamboo Cleaners", "Artisanal Cold Brew"], "cats": ["Household", "Snacks"]}
    ]
    
    precisions = []
    diversities = []
    
    for case in test_cases:
        p_at_k = calculate_precision_at_k(case["purchased"], case["recommended"], k=3)
        div = calculate_catalog_diversity(case["cats"])
        precisions.append(p_at_k)
        diversities.append(div)
        
        print(f"User [{case['user']}] -> Precision@3: {p_at_k} | Category Diversity: {div}")
        
    avg_p = round(sum(precisions) / len(precisions), 4)
    avg_div = round(sum(diversities) / len(diversities), 4)
    
    print("\n" + "-" * 75)
    print(f" Mean Precision@3: {avg_p * 100}%")
    print(f" Catalog Diversity Index: {avg_div}")
    print("-" * 75)
    
    return {"precision_at_3": avg_p, "diversity_index": avg_div}

if __name__ == "__main__":
    run_offline_evaluation()
