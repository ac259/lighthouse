from src.spin_doctor.fact_check import fetch_fact_check, search_wikipedia, analyze_style, check_source_credibility
from src.spin_doctor.llm_analysis import load_local_llm, analyze_with_llm
from src.spin_doctor.search import search_online


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
    
    # Step 6: Load and use Local LLM for final judgment
    llm_pipeline = load_local_llm()
    result["Final Judgment (Local LLM)"] = analyze_with_llm(llm_pipeline, text, result)
    
    return result