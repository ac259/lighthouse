# Hate Inc.

## Why Perspective API?
- **Free & Accessible**: Perspective API is a free machine learning tool that identifies "toxic" comments, helping foster better online conversations.
- **Trusted Partners**: Used by organizations like **The New York Times**, **Wikipedia**, and **The Guardian**.
- **Potential Future Costs**: Currently free, but high Query Per Second (QPS) usage may incur fees in the future.
- **Getting Started**: Follow the official guide at [Perspective API](https://www.perspectiveapi.com/).

---

## 🔹 **Open-Source Alternatives (Local Models)**
Since Perspective API access isn't instant, we integrated **local hate speech detection models**.

### ✅ **1. `facebook/roberta-hate-speech-dynabench-r4-target`**
- **Model Type**: Fine-tuned **RoBERTa** model.
- **Function**: Detects **hate speech, offensive language, or neutral speech**.
- **Source**: Hosted on [Hugging Face](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target).

### ✅ **2.GroNLP/hateBERT
- **Model Type**: Fine-tuned BERT model trained on hateful content.
- **Function**: Detects Hate Speech vs. Non-Hate Speech.
- **Source**: Hosted on Hugging Face.
