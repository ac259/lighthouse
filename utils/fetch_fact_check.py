import requests
import os
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")

# Function to fetch fact-checking data from an external API
def fetch_fact_check(text):
    api_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": text,
        "key": FACT_CHECK_API_KEY
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "claims" in data and len(data["claims"]) > 0:
            return data["claims"][0]["text"]
    return None

def search_wikipedia(query):
    """
    Fetches Wikipedia summary for a given query to verify credibility.
    """
    wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(wiki_api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No Wikipedia information available.")
    return "No Wikipedia information available."

def check_fake_news(text):
    """
    Combines multiple verification sources (Fact Check API, Wikipedia, and LLM)
    to determine the credibility of a given news statement.
    """
    result = []
    # Step 1: Check Google Fact Check API
    fact_check_result = fetch_fact_check(text)
    if fact_check_result:
        result.extend({"source": "Google Fact Check API", "result": fact_check_result})
    
    # Step 2: Search Wikipedia for credibility
    wikipedia_info = search_wikipedia(text)
    dirname = os.path.dirname(os.getcwd())
    model_path = os.path.join(dirname, 'models/bert_fake_news')
    # Step 3: Use an LLM to classify credibility
    classifier = pipeline("text-classification", model=model_path)

    model_result = classifier(text)
    
    return result.extend({
        "source": "LLM and Wikipedia", 
        "wikipedia": wikipedia_info,
        "model_prediction": model_result
    })

def main():
    query = 'Trump is not the president!'
    response = check_fake_news(query)
    print(f'Fact check response : {response}')

if __name__ == '__main__':
    main()