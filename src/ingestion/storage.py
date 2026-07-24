import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

def save_raw_data(data: list, source_name: str) -> str:
    """
    Saves raw ingested data list into a JSON file under data/raw/{source_name}/.
    If S3 environment variables are provided, it can also upload to S3 bucket.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = RAW_DATA_DIR / source_name
    target_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = target_dir / f"{source_name}_reviews_{timestamp}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"[{source_name.upper()}] Successfully saved {len(data)} records to {file_path}")
    return str(file_path)
