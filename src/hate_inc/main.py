from src.hate_inc.analyze_toxicity import analyze_toxicity
from src.hate_inc.detect_hate_speech import detect_hate_speech
from src.hate_inc.llm_hate_speech_analysis import llama_hate_speech_analysis

def analyze_text(text):
    roberta_result = analyze_toxicity(text)
    hatebert_result = detect_hate_speech(text)
    gpt_result = llama_hate_speech_analysis(text)

    return {
        "Roberta": roberta_result,
        "HateBERT": hatebert_result,
        "GPT-4 Analysis": gpt_result
    }
