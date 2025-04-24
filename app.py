from fastapi import FastAPI
from api import router as email_router

app = FastAPI(title="Email Classifier")

app.include_router(email_router, prefix="/email")


