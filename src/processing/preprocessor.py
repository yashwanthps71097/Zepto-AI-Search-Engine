import re

def clean_text(text: str) -> str:
    """
    Cleans raw review text, scrubs potential PII (emails, phone numbers), 
    and standardizes spacing.
    """
    if not text or not isinstance(text, str):
        return ""
        
    # Remove Email addresses
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', text)
    # Remove Phone numbers (Indian format 10 digits or with country code)
    text = re.sub(r'(\+91[\-\s]?)?[6-9]\d{9}', '[REDACTED_PHONE]', text)
    # Normalize extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
