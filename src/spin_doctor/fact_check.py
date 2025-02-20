import requests
import os
import tldextract
import textstat
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys
FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")

# Function to fetch fact-checking data from Google Fact Check API
def fetch_fact_check(text):
    """
    Queries Google Fact Check API to validate a given statement.
    """
    api_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {"query": text, "key": FACT_CHECK_API_KEY}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "claims" in data and len(data["claims"]) > 0:
            return [claim["text"] for claim in data["claims"]]  # Return multiple claims for better accuracy
    return ["No relevant fact-check found."]


# Check credibility of sources
def check_source_credibility(results):
    """
    Evaluates domain credibility based on a predefined list of reputable sources.
    """
    credible_domains = {
        "bbc.com", "nytimes.com", "theguardian.com", "reuters.com",
        "apnews.com", "washingtonpost.com", "forbes.com", "npr.org",
        "cbsnews.com", "abcnews.go.com", "nbcnews.com", "usatoday.com",
        "latimes.com", "bloomberg.com", "wsj.com"
    }
    
    credibility_results = {}

    for title, url, content in results:
        if url:
            extracted_domain = tldextract.extract(url).registered_domain
            if extracted_domain in credible_domains:
                credibility_results[url] = "Credible"
            else:
                credibility_results[url] = "Not Credible"
    
    return credibility_results

# Function to fetch Wikipedia summary
def search_wikipedia(query):
    """
    Fetches Wikipedia summary for a given query to verify credibility.
    """
    wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(wiki_api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No relevant Wikipedia information available.")
    return "No relevant Wikipedia information available."

# Analyze writing style for fake news indicators
def analyze_style(text):
    """
    Uses text statistics to detect overly emotional or misleading writing styles.
    """
    reading_ease = textstat.flesch_reading_ease(text)
    difficult_words = textstat.difficult_words(text)
    return {"Reading Ease Score": reading_ease, "Difficult Words Count": difficult_words}
