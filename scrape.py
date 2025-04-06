from playwright.sync_api import sync_playwright
import requests

def scrape_sbsolver(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        words = page.locator("div.bee-lexicon.bee-entry.bee-cell-first.bee-hover a").all_text_contents()
        #words = page.locator("div").all_text_contents()

        browser.close()

        return words
    
def scrape_full_dict(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()