import json
import csv

def convert_json_to_csv():
    # Load the enriched insights
    with open('dashboard/zepto_enriched_insights.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define CSV headers
    headers = ['Source', 'Original Review Content', 'Cleaned Content', 'Sentiment', 'Friction Barrier Tag', 'Extracted Unmet Need', 'AI Summary']
    
    # Process each review
    rows = []
    for item in data:
        source = item.get('source', '')
        content = item.get('content', '')
        cleaned = item.get('cleaned_content', '')
        
        # Extract from nested AI enrichment
        ai_enrich = item.get('ai_enrichment', {})
        sentiment = ai_enrich.get('sentiment', item.get('sentiment', ''))
        barrier = ai_enrich.get('purchase_barrier', item.get('barrier', ''))
        unmet = ai_enrich.get('unmet_need', '')
        summary = ai_enrich.get('summary', '')
        
        rows.append([source, content, cleaned, sentiment, barrier, unmet, summary])
        
    # Write to CSV
    with open('dashboard/zepto_reviews_readable.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("CSV conversion complete! Saved to dashboard/zepto_reviews_readable.csv")

if __name__ == '__main__':
    convert_json_to_csv()
