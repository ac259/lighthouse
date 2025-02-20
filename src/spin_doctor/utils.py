import requests
import time
import urllib.parse
import urllib.robotparser
import logging
import trafilatura
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, HTTPError, Timeout


logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR)


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

