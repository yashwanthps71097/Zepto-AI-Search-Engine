import sys
import json
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.processing.absa_enricher import enrich_review_record
from src.processing.vector_indexer import generate_and_store_embeddings

RAW_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
ENRICHED_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "enriched"

def run_phase_2_processing(max_records_per_source: int = 5):
    """
    Orchestrates Phase 2: Reads raw ingested JSON files from data/raw/,
    runs PII scrubbing, invokes Groq LPU API for ABSA & barrier analysis,
    formats vector embeddings, and saves outputs to data/enriched/.
    """
    print("=" * 75)
    print("    ZEPTO DISCOVERY ENGINE - PHASE 2 AI ENRICHMENT (GROQ LLM PIPELINE)")
    print("=" * 75)
    
    ENRICHED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_enriched_records = []
    
    if not RAW_DATA_DIR.exists():
        print("[ERROR] data/raw directory not found. Run Phase 1 ingestion first!")
        return

    # Find raw JSON files
    raw_files = list(RAW_DATA_DIR.glob("**/*.json"))
    if not raw_files:
        print("[ERROR] No raw JSON data files found in data/raw/. Run Phase 1 ingestion first!")
        return

    print(f"Found {len(raw_files)} raw dataset files. Processing batches with Groq LLM...\n")

    for file_path in raw_files:
        source_name = file_path.parent.name
        print(f"---> Processing dataset file: [{source_name}] {file_path.name}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Process subset per file for testing/validation
        sample_batch = data[:max_records_per_source] if max_records_per_source else data
        
        for item in sample_batch:
            print(f"  [AI ENRICHING] Analyzing item: ID {item.get('review_id') or item.get('post_id') or item.get('ticket_id')}...")
            enriched = enrich_review_record(item)
            all_enriched_records.append(enriched)

    # Save enriched dataset
    output_file = ENRICHED_DATA_DIR / "zepto_enriched_insights.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_enriched_records, f, ensure_ascii=False, indent=2)
        
    print(f"\n[ENRICHMENT SUCCESS] Saved {len(all_enriched_records)} enriched records to {output_file}")
    
    # Run Vector Indexing step
    generate_and_store_embeddings(all_enriched_records)
    
    print("\n" + "=" * 75)
    print(" Phase 2 AI Enrichment Pipeline Complete!")
    print(f" Enriched Data Saved at: data/enriched/zepto_enriched_insights.json")
    print("=" * 75)

if __name__ == "__main__":
    run_phase_2_processing(max_records_per_source=3)
