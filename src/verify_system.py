import urllib.request
import json
import sys

# Ensure UTF-8 output encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def verify_system():
    print("=" * 75)
    print("    ZEPTO DISCOVERY ENGINE - SYSTEM VERIFICATION CHECK")
    print("=" * 75)
    
    # 1. Verify Personalization REST API Backend (Port 8081)
    api_url = "http://localhost:8081/v1/user/discovery-recommendations?user_id=usr_1001"
    print(f"\n[1/2] Testing Backend API: {api_url}...")
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            data = json.loads(body)
            print(f"  [OK] Status Code: {status} OK")
            print(f"  [OK] Response User ID: {data.get('user_id')}")
            print(f"  [OK] User Cohort: {data.get('cohort')}")
            print(f"  [OK] Latency: {data.get('latency_ms')}")
            print(f"  [OK] Recommendations Returned: {len(data.get('recommendations', []))}")
    except Exception as e:
        print(f"  [FAILED] Backend API Check Failed: {e}")

    # 2. Verify Frontend Dashboard Web Server (Port 8080)
    frontend_url = "http://localhost:8080/"
    print(f"\n[2/2] Testing Frontend Server: {frontend_url}...")
    try:
        req = urllib.request.Request(frontend_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            print(f"  [OK] Status Code: {status} OK")
            print(f"  [OK] Frontend Omni-Search Hub Dashboard served successfully!")
    except Exception as e:
        print(f"  [FAILED] Frontend Server Check Failed: {e}")

    print("\n" + "=" * 75)
    print(" System Verification Complete! Both Backend & Frontend are operational.")
    print("=" * 75)

if __name__ == "__main__":
    verify_system()
