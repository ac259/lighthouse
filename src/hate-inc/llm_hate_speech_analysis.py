from gpt4all import GPT4All

MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

def llama_hate_speech_analysis(text):
    try:
        model = GPT4All(MODEL_NAME)
        
        prompt = f"""
        [INST] You are a hate speech detection assistant. Analyze the following text and determine if it contains hate speech.
        Provide a classification and brief explanation.

        Text: "{text}"
        [/INST]
        """
        
        response = model.generate(prompt, max_tokens=200, temp=0.7)
        return response.strip()
    
    except Exception as e:
        return f"Error analyzing text: {e}"

