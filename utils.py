import re

# Regex patterns for detecting various types of PII (Personally Identifiable Information)
patterns = {
    "full_name": r"\b([A-Z][a-z]+(?:\s(?:[A-Z][a-z]+|[A-Z]))+)\b",  # Full names (first and last)
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",  # Email addresses
    "phone_number": r"\b(?:\+91[-\s]?|0)?[6789]\d{9}\b",  # Indian phone numbers
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",  # Date of birth (DD/MM/YYYY or DD-MM-YYYY)
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Aadhar number (Indian identity)
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",  # Credit/Debit card numbers
    "cvv_no": r"\b\d{3}\b",  # CVV code
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2}\b"  # Expiry date for cards (MM/YY)
}

# Common name introducers that help identify if a string is likely a name
name_introducers = [
    "my name is", "i am", "called me", "this is", "contact me",
    "reach me at", "from", "sincerely", "regards", "yours truly"
]

def is_likely_name(text, context):
    """
    Determines if a string is likely a name based on casing and context.
    
    Args:
    - text (str): The potential name to verify.
    - context (str): The surrounding text to examine for clues.
    
    Returns:
    - bool: True if the text is likely a name, otherwise False.
    """
    # Check if text follows the pattern for a name (capitalized first letter, followed by lowercase)
    if not re.fullmatch(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", text):
        return False

    # Check if the text appears in the context with common name introducers
    context = context.lower()
    name_pos = context.find(text.lower())
    preceding_text = context[max(0, name_pos - 30):name_pos]

    return any(intro in preceding_text for intro in name_introducers)

def mask_pii(text):
    """
    Masks PII including one-word and full names based on context.
    
    Args:
    - text (str): The input text containing potential PII to mask.
    
    Returns:
    - str: The text with PII masked.
    - list: A list of dictionaries containing information about the masked entities.
    """
    masked_text = text
    entities = []

    # Detect all capitalized words or phrases that could be full names
    possible_names = re.finditer(patterns["full_name"], text)
    for match in possible_names:
        original = match.group()
        start, end = match.start(), match.end()

        # Extract the surrounding context for the potential name
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        context = text[context_start:context_end]

        # If the name is not likely a name based on context, skip masking
        if not is_likely_name(original, context):
            continue

        # Mask the full name
        masked_text = masked_text[:start] + "[full_name]" + masked_text[end:]
        shift = len("[full_name]") - len(original)
        
        # Record the masked entity
        entities.append({
            "position": [start, start + len("[full_name]")],
            "classification": "full_name",
            "entity": original
        })

        # Update positions of other entities after text shift due to the replacement
        for m in entities:
            if m["position"][0] > start:
                m["position"][0] += shift
                m["position"][1] += shift

    # Mask other types of PII (email, phone numbers, etc.)
    for label, pattern in patterns.items():
        if label == "full_name":
            continue  # Skip full names as they are already processed

        for match in re.finditer(pattern, masked_text):
            original = match.group()
            start, end = match.start(), match.end()

            # Skip entities that are already masked in the same region
            if any(e["position"][0] <= start < e["position"][1] for e in entities):
                continue

            # Mask the PII entity
            masked_text = masked_text[:start] + f"[{label}]" + masked_text[end:]
            shift = len(f"[{label}]") - len(original)

            # Record the masked entity
            entities.append({
                "position": [start, start + len(f"[{label}]")],
                "classification": label,
                "entity": original
            })

            # Update positions of other entities due to the text shift
            for m in entities:
                if m["position"][0] > start:
                    m["position"][0] += shift
                    m["position"][1] += shift

    return masked_text, entities
