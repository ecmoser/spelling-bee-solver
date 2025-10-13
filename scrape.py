from playwright.sync_api import sync_playwright, Page
import requests

def scrape_sbsolver(url, page: Page):
    page.goto(url, wait_until="domcontentloaded")
    words_counts = list(zip(page.locator("div.bee-lexicon.bee-entry.bee-cell-first.bee-hover a").all_text_contents(),
                       page.locator("div.bee-lexicon.bee-count-fixed.bee-cell").all_text_contents()))
    # words = page.locator("div.bee-lexicon.bee-entry.bee-cell-first.bee-hover a").all_text_contents()
    words = [a[0] for a in words_counts if not "*" in a[1]]
    return words
    
def scrape_full_dict(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()