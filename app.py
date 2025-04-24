from fastapi import FastAPI
from api import router as email_router

app = FastAPI(title="Email Classifier")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Classifier API!"}

app.include_router(email_router, prefix="/email")


