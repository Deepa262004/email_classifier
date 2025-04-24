from fastapi import APIRouter
from pydantic import BaseModel
from models import classify_email

router = APIRouter()


class EmailInput(BaseModel):
    email_body: str


@router.post("/")
def process_email(input_data: EmailInput):
    result = classify_email(input_data.email_body)
    return result
