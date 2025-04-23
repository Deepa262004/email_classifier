from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle
from utils import mask_pii

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("models/")
tokenizer = AutoTokenizer.from_pretrained("models/")

# Load label encoder
with open("models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


def classify_email(email_body: str):
    """
    Classify the category of an email after masking PII information.

    Args:
        email_body (str): Raw email content.

    Returns:
        dict: Dictionary containing original email, masked email, detected entities,
              and the predicted category.
    """
    masked_email, entity_list = mask_pii(email_body)
    inputs = tokenizer(
        masked_email,
        return_tensors="pt",
        truncation=True,
        padding=True
    )
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()

    category = label_encoder.inverse_transform([pred])[0]

    return {
        "input_email_body": email_body,
        "list_of_masked_entities": entity_list,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
