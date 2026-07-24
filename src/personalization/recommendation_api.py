import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from src.personalization.feature_store import feature_store
from src.personalization.hook_generator import hook_generator

CATALOG = [
    {
        "product_id": "p_101",
        "name": "Organic Farm Fresh Apples",
        "category": "Produce",
        "price": "₹149",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300"
    },
    {
        "product_id": "p_102",
        "name": "Gourmet Aged Cheddar Cheese",
        "category": "Gourmet",
        "price": "₹199",
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300"
    },
    {
        "product_id": "p_103",
        "name": "Eco-Friendly Bamboo Cleaners",
        "category": "Household",
        "price": "₹249",
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300"
    }
]

def get_recommendations_for_user(user_id: str) -> dict:
    """
    Core personalization engine algorithm:
    1. Fetches user features & barrier vectors from Feast Feature Store.
    2. Selects out-of-habit products matching high-affinity new category.
    3. Generates personalized dynamic hooks via DynamicHookGenerator.
    """
    start_time = time.time()
    
    # Step 1: Feature Lookup (<2ms)
    uf = feature_store.get_user_features(user_id)
    cohort = uf.get("cohort")
    target_category = uf.get("affinity_category")
    barrier = uf.get("top_barrier")
    
    # Step 2: Match Product from Catalog
    recommended_items = []
    for item in CATALOG:
        if item["category"] == target_category or not recommended_items:
            hook = hook_generator.generate_hook(barrier, item["category"], item["name"])
            recommended_items.append({
                **item,
                "dynamic_hook": hook,
                "targeted_cohort": cohort,
                "barrier_addressed": barrier
            })
            
    latency_ms = round((time.time() - start_time) * 1000, 2)
    
    return {
        "status": "success",
        "user_id": user_id,
        "cohort": cohort,
        "latency_ms": f"{latency_ms} ms",
        "recommendations": recommended_items
    }

class PersonalizationAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/v1/user/discovery-recommendations":
            query_params = parse_qs(parsed_url.query)
            user_id = query_params.get("user_id", ["usr_1001"])[0]
            
            res_data = get_recommendations_for_user(user_id)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res_data, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Endpoint not found"}')

def run_recommendation_api_server(port: int = 8081):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PersonalizationAPIHandler)
    print(f"[PERSONALIZATION API] Serving /v1/user/discovery-recommendations on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_recommendation_api_server()
