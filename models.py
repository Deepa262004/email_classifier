from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle
from utils import mask_pii

model = AutoModelForSequenceClassification.from_pretrained("Deepa2426/classify_model", revision="master")
tokenizer = AutoTokenizer.from_pretrained("Deepa2426/classify_model", revision="master")


# Load label encoder from the uploaded file
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

def model_train_code():
    """
    Trains a sequence classification model using the Hugging Face Transformers library
    and saves the model, tokenizer, and label encoder.

    This function performs the following tasks:
    1. Loads and preprocesses the email dataset.
    2. Masks PII (Personally Identifiable Information) from the email text.
    3. Tokenizes the text using a pre-trained tokenizer.
    4. Trains a sequence classification model.
    5. Saves the trained model, tokenizer, and label encoder.
    """
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
    from datasets import Dataset
    from sklearn.preprocessing import LabelEncoder
    import pandas as pd
    import torch
    import pickle

    # Load and preprocess data
    df = pd.read_csv("/content/combined_emails_with_natural_pii.csv")
    
    # Mask PII in the email text
    df["text"] = df["email"].apply(lambda x: mask_pii(x)[0])  # PII masking function
    
    # Encode labels using LabelEncoder
    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["type"])
    
    # Create a Dataset from the pandas DataFrame
    dataset = Dataset.from_pandas(df[["text", "label"]])
    
    # Initialize the tokenizer and model
    model_name = "xlm-roberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Define tokenization function
    def tokenize_function(examples):
        """
        Tokenizes the input text by padding and truncating to the maximum length.
        """
        return tokenizer(examples["text"], padding="max_length", truncation=True)
    
    # Apply the tokenization to the dataset
    dataset = dataset.map(tokenize_function, batched=True)
    
    # Split the dataset into training and testing sets
    dataset = dataset.train_test_split(test_size=0.2)
    
    # Load the pre-trained model for sequence classification
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_encoder.classes_)
    )
    
    # Set up the training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        logging_dir="./logs"
    )
    
    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        tokenizer=tokenizer
    )
    
    # Train the model
    trainer.train()

    # Save the trained model and tokenizer
    trainer.save_model("./final_model")
    model.save_pretrained("model/")
    tokenizer.save_pretrained("model/")
    
    # Save the label encoder
    with open("model/label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)
