
# 📧 Email Classification

This project implements an **email classification system** for a support team. It classifies incoming emails into predefined categories such as **Incident**, **Request**, and **Problem**, while ensuring that any **Personally Identifiable Information (PII)** is masked before processing.

---

## 🚀 Features

- 🔐 **PII Masking** using Regex (non-LLM approach)
- 📊 **Text Classification** using `XLM-RoBERTa` (for multilingual emails)
- 🌐 **FastAPI** based API endpoint
- 🧠 **Model Training** using Hugging Face Transformers
- 📁 **Well-structured codebase**
- 📤 **Deployed model-ready structure for Hugging Face Spaces**

---

## 📂 Project Structure

email-classifier/ 
├── app.py # FastAPI entrypoint 
├── utils.py # PII masking logic
├── emails.csv # Sample dataset 
├── requirements.txt # Python dependencies 
├── README.md # Setup and usage instructions 
├── models/ # Saved model and tokenizer │ ├
  ── label_encoder.pkl │ └── tokenizer/

---

## 🛠️ Setup Instructions

### 
1. Clone the Repository
  
  git clone https://github.com/Deepa262004/email_classifier.git
  cd email_classifier

2. Install Dependencies
  pip install -r requirements.txt

3. Run the API
  uvicorn app:app --reload
  The API will be accessible at:
  http://127.0.0.1:8000


📤 API Input Format
    Send a POST request to /email/process i.e., http://127.0.0.1:8000/email/process  using POSTMAN or others with this JSON structure:
    json
    {
      "email_body": "Subject: Help needed. My name is John Doe. Please assist. You can reach me at john@example.com."
    }

📥 API Output Format
    json
    {
      "input_email_body": "...",
      "list_of_masked_entities": [
        {
          "position": [start_index, end_index],
          "classification": "entity_type",
          "entity": "original_value"
        }
      ],
      "masked_email": "...",
      "category_of_the_email": "..."
    }


  or 
  
🌐 Try it on Hugging Face Spaces

1. Open the deployment URL:
  👉https://deepa2426-email-classification.hf.space/docs

2. Select method as POST

3. Use the following format JSON in the body:
  json: {
    "email_body": "Dear team, I noticed unauthorized activity on my account and several transactions I did not make. Please investigate this issue immediately and let me know the next steps. Regards, Alex Raji"
  }

  






