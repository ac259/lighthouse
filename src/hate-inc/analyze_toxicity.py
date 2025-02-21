import requests
import os
from transformers import pipeline

PERSPECTIVE_API_KEY = "your_api_key_here"
# Load the model
toxicity_classifier = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

def analyze_toxicity(text):
    result = toxicity_classifier(text)[0]  # Extract first result
    return {"label": result["label"], "score": round(result["score"], 2)}

def analyze_toxicity_persepctive(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {}, 
            "INSULT": {}, 
            "IDENTITY_ATTACK": {}, 
            "PROFANITY": {}
        }
    }
    response = requests.post(url, json=data, params={"key": PERSPECTIVE_API_KEY})
    return response.json()
