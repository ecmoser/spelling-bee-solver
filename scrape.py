from playwright.sync_api import sync_playwright, Page
import requests


def scrape_site(url, page: Page):
    page.goto(url, wait_until="domcontentloaded")
    words = page.locator("tr td:nth-child(1)").all_text_contents()
    return words


def scrape_full_dict(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()
