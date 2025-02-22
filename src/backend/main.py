import sys
import os
from fastapi.middleware.cors import CORSMiddleware

# Ensure src/ is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from backend.routes.hate_speech import router as hate_speech_router
from backend.routes.fake_news import router as fake_news_router
import uvicorn

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Register API routes
app.include_router(hate_speech_router, prefix="/api")
app.include_router(fake_news_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
