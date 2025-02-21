from fastapi import APIRouter
from pydantic import BaseModel
from hate_inc.main import analyze_text

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/analyze-hate-speech")
async def detect_hate_speech(input_text: TextInput):
    """
    API Route to analyze text for hate speech.
    """
    result = analyze_text(input_text.text)
    return result
