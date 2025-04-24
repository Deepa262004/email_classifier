
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
<pre>
email-classifier/ 
├── app.py # FastAPI entrypoint 
├── utils.py # PII masking logic
├── emails.csv # Sample dataset 
├── requirements.txt # Python dependencies 
├── README.md # Setup and usage instructions 
├── models/ # Saved model and tokenizer │
  ├── label_encoder.pkl
  │── tokenizer/
</pre>
---

## 🛠️ Setup Instructions

### 
1. Clone the Repository
  
 <pre> 
    git clone https://github.com/Deepa262004/email_classifier.git
    cd email_classifier
   </pre>

2. Install Dependencies
  <PRE>pip install -r requirements.txt</PRE>

3. Run the API
  <PRE>uvicorn app:app --host 0.0.0.0 --port 8000</PRE>
  The API will be accessible at:
  http://127.0.0.1:8000


📤 API Input Format
    Send a POST request to /email/process i.e., http://127.0.0.1:8000/email/  using POSTMAN or others with this JSON structure:
    json
     <pre>
    {
      "email_body": "Subject: Help needed. My name is John Doe. Please assist. You can reach me at john@example.com."
    }</pre>

📥 API Output Format
   json
    <pre> {
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
</pre>

# OR
  
🌐 Try it on Hugging Face Spaces

1. Open the deployment URL:
  👉[https://deepa2426-email-classification.hf.space/docs](https://deepa2426-email-classification.hf.space/docs)
2. input ur email body as string(it shld be a continuous string without any line breaks for proper json)
3. run it

To try it in postman or thumbnail:

1. Copy the deployment URL:
  👉[https://deepa2426-email-classification.hf.space/](https://deepa2426-email-classification.hf.space/)

2. Set Method: POST
 In the Body Tab: Select raw
 Choose JSON from the dropdown

  json
 <pre>{
    "email_body": " Hello, I forgot my password and would like to reset it. My name is John Doe. Please assist. You can reach me at johndoe@example.com."
  } </pre> 

 # Avoid the following format:
   json
  <pre> ```json { "email_body": " Hello, I forgot my password and would like to reset it.
    My name is John Doe. Please assist. You can reach me at johndoe@example.com." } ``` </pre>








