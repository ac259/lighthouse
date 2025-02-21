import sys
import os

# Ensure src/ is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from backend.routes.hate_speech import router as hate_speech_router
import uvicorn

app = FastAPI()

# Register API routes
app.include_router(hate_speech_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
