import re

# Regex patterns
patterns = {
    "full_name": r"\b([A-Z][a-z]+(?:\s(?:[A-Z][a-z]+|[A-Z]))+)\b", 
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "phone_number": r"\b(?:\+91[-\s]?|0)?[6789]\d{9}\b",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2}\b"
}

# Common name introducers
name_introducers = [
    "my name is", "i am", "called me", "this is", "contact me",
    "reach me at", "from", "sincerely", "regards", "yours truly"
]

def is_likely_name(text, context):
    """
    Determines if a string is likely a name based on casing and context.
    """
    if not re.fullmatch(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", text):
        return False

    context = context.lower()
    name_pos = context.find(text.lower())
    preceding_text = context[max(0, name_pos - 30):name_pos]

    return any(intro in preceding_text for intro in name_introducers)

def mask_pii(text):
    """
    Masks PII including one-word and full names based on context.
    """
    masked_text = text
    entities = []

    # Detect all capitalized words or phrases
    possible_names = re.finditer(patterns["full_name"], text)
    for match in possible_names:
        original = match.group()
        start, end = match.start(), match.end()

        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        context = text[context_start:context_end]

        if not is_likely_name(original, context):
            continue

        masked_text = masked_text[:start] + "[full_name]" + masked_text[end:]
        shift = len("[full_name]") - len(original)
        entities.append({
            "position": [start, start + len("[full_name]")],
            "classification": "full_name",
            "entity": original
        })

        # update remaining matches due to text shift
        for m in list(entities):
            if m["position"][0] > start:
                m["position"][0] += shift
                m["position"][1] += shift

    # Mask other types of PII
    for label, pattern in patterns.items():
        if label == "full_name":
            continue

        for match in re.finditer(pattern, masked_text):
            original = match.group()
            start, end = match.start(), match.end()

            if any(e["position"][0] <= start < e["position"][1] for e in entities):
                continue

            masked_text = masked_text[:start] + f"[{label}]" + masked_text[end:]
            shift = len(f"[{label}]") - len(original)
            entities.append({
                "position": [start, start + len(f"[{label}]")],
                "classification": label,
                "entity": original
            })

            for m in list(entities):
                if m["position"][0] > start:
                    m["position"][0] += shift
                    m["position"][1] += shift

    return masked_text, entities
