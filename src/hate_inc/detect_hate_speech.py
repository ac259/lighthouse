from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

MODEL_NAME = "GroNLP/hateBERT"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def detect_hate_speech(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    
    labels = ["Not Hate Speech", "Hate Speech"]
    return labels[prediction]

