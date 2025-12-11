from playwright.sync_api import sync_playwright
import os

URL = 'http://127.0.0.1:5500/ui_demo_output.html'
OUT = 'ui_demo_output.png'

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        # wait a bit for styles
        page.wait_for_timeout(400)
        page.screenshot(path=OUT, full_page=True)
        print('Saved screenshot', OUT)
        browser.close()

if __name__ == '__main__':
    main()
