import re

# Define regex patterns for different entities
patterns = {
    "full_name": r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b",
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "phone_number": r"\b(?:\+91[-\s]?|0)?[6789]\d{9}\b",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2}\b"
}


def is_likely_name(text, context):
    """
    Enhanced name detection focusing on common name patterns.
    Returns True if the text is likely to be a full name.
    """
    # Must be two capitalized words
    if not re.fullmatch(r'[A-Z][a-z]+\s[A-Z][a-z]+', text):
        return False

    # Check for explicit name introduction patterns
    name_introducers = [
        "my name is", "i am", "called me", "this is", "contact me",
        "reach me at", "from", "sincerely", "regards", "yours truly"
    ]

    # Look at the preceding 20 characters for name indicators
    preceding_text = context[:context.lower().find(text.lower())][-20:].lower()

    # If found after a name introducer phrase, definitely a name
    return any(introducer in preceding_text for introducer in name_introducers)


def mask_pii(text):
    """
    Masks personally identifiable information (PII) in the input text.
    Returns the masked text and a list of identified entities.
    """
    masked_text = text
    entities = []

    # First pass: detect and mask full names with enhanced detection
    for match in re.finditer(patterns["full_name"], masked_text):
        original = match.group()
        start, end = match.start(), match.end()

        # Get surrounding context (50 chars before and after)
        context_start = max(0, start - 50)
        context_end = min(len(masked_text), end + 50)
        context = masked_text[context_start:context_end]

        if not is_likely_name(original, context):
            continue

        masked_text = masked_text[:start] + "[full_name]" + masked_text[end:]
        entities.append({
            "position": [start, start + len("[full_name]")],
            "classification": "full_name",
            "entity": original
        })

    # Mask other entities
    for label, pattern in patterns.items():
        if label == "full_name":
            continue

        for match in re.finditer(pattern, masked_text):
            original = match.group()
            start, end = match.start(), match.end()

            # Skip if this range is already masked
            if any(e["position"][0] <= start < e["position"][1] for e in entities):
                continue

            masked_text = masked_text[:start] + f"[{label}]" + masked_text[end:]
            entities.append({
                "position": [start, start + len(f"[{label}]")],
                "classification": label,
                "entity": original
            })

    return masked_text, entities
