from gpt4all import GPT4All

MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

# Generate a final judgment using local LLM
def analyze_with_llm(llm_pipeline, query, sources):
    """
    Uses a local LLM to analyze aggregated data and make a final judgment.
    """
   # Define system and user prompts
    system_prompt = (
        "You are a fake news detection assistant. Your goal is to analyze a claim using multiple sources and determine its credibility."
    )

    user_prompt = (
        f"Claim: {query}\n\n"
        f"Sources:\n"
        f"- Google Fact Check: {sources['Google Fact Check API']}\n"
        f"- Wikipedia: {sources['Wikipedia']}\n"
        f"- Online Search: {sources['Online Search']}\n"
        f"- Writing Style Analysis: {sources['Style Analysis']}\n"
        f"- Source Credibility: {sources['Source Credibility']}\n\n"
        "Based on these sources, analyze whether the claim is true or false. Provide a confidence level and explanation."
    )

    # Combine system and user prompts into the final prompt
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        f"{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    )

    
    response = llm_pipeline.generate(prompt, max_tokens=1000)
    # print(f'LLM analysed respnse is : {response}')
    return response

# Load local GPT4All LLM model
def load_local_llm():
    """
    Loads a local GPT4All model for final judgment.
    """
    return GPT4All(MODEL_NAME)

def summarize_text(text, max_length=100):
    """
    Summarizes the given text using the specified Mistral model.

    Args:
        text (str): The text to be summarized.
        max_length (int): The maximum length of the summary.

    Returns:
        str: The summary of the text.
    """
    try:
        # Initialize the GPT4All model
        model = GPT4All(model_name=MODEL_NAME)

        # Define the prompt for summarization
        prompt = f"<s>[INST] Summarize the following text:\n\n{text}\n\n[/INST]"

        # Generate the summary
        response = model.generate(prompt, max_tokens=max_length, temp=0.7)

        return response[:max_length]
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None