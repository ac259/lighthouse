from fastapi import APIRouter
from pydantic import BaseModel
from spin_doctor.main import check_fake_news

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/detect-fake-news")
async def detect_hate_speech(input_text: TextInput):
    """
    API Route to analyze text for hate speech.
    """
    result = check_fake_news(input_text.text)
    return result
