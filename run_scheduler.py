import time
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure UTF-8 output encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent

# Define Indian Standard Time (IST) timezone: UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))

def get_seconds_until_10am_ist() -> int:
    """Calculates the number of seconds from the current moment until 10:00 AM IST."""
    now = datetime.now(IST)
    target = now.replace(hour=10, minute=0, second=0, microsecond=0)
    # If it's already past 10:00 AM IST today, schedule for 10:00 AM IST tomorrow
    if now >= target:
        target += timedelta(days=1)
    diff = target - now
    return int(diff.total_seconds())

def run_pipeline_step(module_name: str):
    print(f"\n[SCHEDULER] Starting {module_name}...")
    try:
        subprocess.run(
            [sys.executable, "-m", module_name],
            cwd=PROJECT_ROOT,
            check=True
        )
        print(f"[SCHEDULER] {module_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[SCHEDULER ERROR] Failed running {module_name}: {e}")

def run_full_pipeline():
    print("=" * 80)
    print(f"   STARTING SCHEDULED AI ENGINE UPDATE PIPELINE - {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("=" * 80)
    
    # 1. Ingestion
    run_pipeline_step("src.ingestion.main_ingestion")
    
    # 2. AI Processing & LLM Enrichment
    run_pipeline_step("src.processing.main_processing")
    
    # 3. Cohort Analysis & Analytics Summary
    run_pipeline_step("src.analytics.cohort_analyzer")
    
    print("\n" + "=" * 80)
    print(f"   PIPELINE UPDATE CYCLE COMPLETE - {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("=" * 80)

def main():
    print("=" * 80)
    print("      ZEPTO DISCOVERY ENGINE - PRODUCTION DAEMON SCHEDULER")
    print("=" * 80)
    print(f"Current System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current IST Time   : {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("Scheduler Target   : 10:00 AM IST Daily")
    print("=" * 80)
    
    try:
        while True:
            seconds_to_sleep = get_seconds_until_10am_ist()
            next_run_time = datetime.now(IST) + timedelta(seconds=seconds_to_sleep)
            print(f"\n[SCHEDULER] Next execution scheduled for: {next_run_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"[SCHEDULER] Sleeping for {seconds_to_sleep} seconds ({round(seconds_to_sleep/3600, 2)} hours)...")
            
            # Sleep in small increments to allow graceful termination (Ctrl+C)
            slept = 0
            while slept < seconds_to_sleep:
                time.sleep(min(10, seconds_to_sleep - slept))
                slept += 10
            
            run_full_pipeline()
    except KeyboardInterrupt:
        print("\n[SCHEDULER STOPPED] Scheduler daemon terminated by user.")

if __name__ == "__main__":
    main()
