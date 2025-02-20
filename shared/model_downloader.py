import os
from transformers import AutoModelForCausalLM, AutoTokenizer



model_name = "mistralai/Mistral-7B-v0.1"  # Replace with your model

tokenizer = AutoTokenizer.from_pretrained(model_name)
dirname = os.path.dirname(os.getcwd())
model_path = os.path.join(dirname, 'models/')
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=model_path)
