from utils import extract_main_content
from duckduckgo_search import DDGS
from itertools import islice
from llm_analysis import summarize_text

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
