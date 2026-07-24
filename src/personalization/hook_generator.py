class DynamicHookGenerator:
    """
    Generates personalized banner text, badges, and promotional copy 
    specifically tailored to overcome a user's category discovery barrier.
    """
    def __init__(self):
        self.templates = {
            "QUALITY_CONCERN": [
                "Farm-fresh guarantee • Checked 3x for quality",
                "100% Organic & Pesticide-free • Packed today",
                "Freshness replacement policy within 10 mins"
            ],
            "HIGH_PRICE": [
                "Trial Pack Offer: 20% off your first try",
                "Value Bundle Savings • Exclusive deal",
                "Pocket-friendly starter size available"
            ],
            "PACK_SIZE_TOO_LARGE": [
                "New 200g Mini Trial Pack available",
                "Single-serve size available now"
            ],
            "HIDDEN_IN_UI": [
                "Trending in your neighborhood this week",
                "Pairs perfectly with your morning order"
            ]
        }

    def generate_hook(self, barrier: str, target_category: str, product_name: str) -> str:
        """
        Returns dynamic badge copy designed to counter the user's specific friction point.
        """
        category_hooks = self.templates.get(barrier, [
            f"Explore top-rated items in {target_category}",
            f"Handpicked recommendation for you"
        ])
        
        # Select first matching dynamic hook template
        return f"{category_hooks[0]} on {product_name}"

hook_generator = DynamicHookGenerator()
