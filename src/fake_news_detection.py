
import requests
import os
import re
import tldextract
import textstat
import urllib.parse
import time
import logging
import trafilatura
from gpt4all import GPT4All
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse, urljoin
from duckduckgo_search import DDGS
from itertools import islice
from requests.exceptions import RequestException, HTTPError, Timeout

logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Load API keys
FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")
MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

def is_allowed_to_scrape(url, user_agent='*'):
    """
    Checks if scraping the given URL is allowed according to the site's robots.txt file.
    """
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = urljoin(base_url, '/robots.txt')

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    return rp.can_fetch(user_agent, url)


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
    
def extract_main_content(url):
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/131.0.0.0 Safari/537.36')

    if not is_allowed_to_scrape(url, user_agent):
        print(f"Scraping disallowed for URL: {url}")
        return None
    try:
        # Fetch the URL content
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            logging.error(f"Failed to download content from {url}")
            return None

        # Extract the main content
        result = trafilatura.extract(downloaded)
        if result is None:
            logging.error(f"Failed to extract content from {url}")
            return None

        return result

    except (RequestException, HTTPError, Timeout) as e:
        logging.error(f"Request error for {url}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred for {url}: {e}")

    return None


def extract_text_from_url(url):
    """
    Extracts and returns the main text content from the specified URL.
    """
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/131.0.0.0 Safari/537.36')

    if not is_allowed_to_scrape(url, user_agent):
        print(f"Scraping disallowed for URL: {url}")
        return None

    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove unwanted elements like scripts and styles
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Extract text
    text = ' '.join(soup.stripped_strings)

    # Polite crawling: delay between requests
    time.sleep(1)  # Sleep for 1 second

    return text

def search_online(query, max_results=3):
    """
    Searches for information online using DuckDuckGo and retrieves content from the top results.
    """
    results = []

    with DDGS() as ddgs:
        ddgs_text_gen = ddgs.text(query, region='wt-wt', safesearch='Moderate')
        for result in islice(ddgs_text_gen, max_results):
            title = result.get('title')
            url = result.get('href')
            if title and url:
                content = extract_main_content(url)
                summarized_content = summarize_text(content)
                if summarized_content:
                    results.append((title, url, summarized_content))

    return results

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

# Load local GPT4All LLM model
def load_local_llm():
    """
    Loads a local GPT4All model for final judgment.
    """
    return GPT4All(MODEL_NAME)

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

# Main function to check fake news
def check_fake_news(text):
    """
    Combines multiple verification sources (Fact Check API, Wikipedia, Online Search, Writing Style, Source Credibility, and Local LLM)
    to determine the credibility of a given news statement.
    """
    result = {}
    
    # Step 1: Check Google Fact Check API
    result["Google Fact Check API"] = fetch_fact_check(text)
    
    # Step 2: Search Wikipedia for credibility
    result["Wikipedia"] = search_wikipedia(text)
    
    # Step 3: Search Online for recent information using DuckDuckGo
    search_results = search_online(text)
    result["Online Search"] = search_results
    
    # Step 4: Analyze writing style
    result["Style Analysis"] = analyze_style(text)
    
    # Step 5: Check source credibility
    result["Source Credibility"] = check_source_credibility(search_results)
    
    print(f'Results prior to passing it to LLM: {result}')
    # Step 6: Load and use Local LLM for final judgment
    llm_pipeline = load_local_llm()
    result["Final Judgment (Local LLM)"] = analyze_with_llm(llm_pipeline, text, result)
    
    return result

def main():
    query_1 = 'Does Kurkure chips have plastic in it?'
    query_2 = 'Eating lots of Carrots turn people to Orange?'
    query_3 = 'Did Trump call Zelensky a dictator?'
    result = check_fake_news(query_3)
    print(result["Final Judgment (Local LLM)"])
    
if __name__ == '__main__':
    main()