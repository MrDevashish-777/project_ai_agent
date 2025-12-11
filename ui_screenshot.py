"""
ui_screenshot.py
Opens the frontend in a headless browser, interacts with the chat flow, and captures a screenshot and HTML snapshot.

Prereqs: Playwright Python should be installed. This script runs headless and saves files:
- ui_chat_screenshot.png
- ui_chat_snapshot.html
"""
from playwright.sync_api import sync_playwright
import time
import os

BASE = os.getenv('AI_AGENT_BASE', 'http://127.0.0.1:5500')
OUT_DIR = os.getcwd()

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Log console messages from the page for debugging
        page.on('console', lambda msg: print('PAGE CONSOLE:', msg.text))
        print('Going to', f"{BASE}/index.html")
        resp = page.goto(f"{BASE}/index.html")
        print('Goto response', resp.status if resp else 'no response')
        # Print the portion of the HTML to confirm presence of elements
        html = page.content()
        print('HTML snippet contains chatbot-icon?', 'chatbot-icon' in html[:800])
        print('HTML snippet length', len(html))
        # wait for the chat icon and open chat
        print('Attempting to click #chatbot-icon...')
        has_icon = page.query_selector('#chatbot-icon')
        if has_icon:
            try:
                page.evaluate("document.getElementById('chatbot-icon').click()")
                print('JS click executed')
            except Exception as e:
                print('JS click error:', e)
        else:
            print('No chatbot icon found to click')
        time.sleep(0.3)
        page.wait_for_selector('#chat-body')

        # We send 'Hi' and 'Budget 2500', then pick the first suggestion and click Book
        # If the page auto-sends 'Hi' on load, that's fine, but we ensure we have messages.
        try:
            # Wait a bit for auto message
            time.sleep(1)
            # Click into input
            page.fill('#chat-input', 'Budget 2500')
            page.click('#send-btn')
            # Wait for bot reply with suggestions
            print('Waiting for suggestion selector')
            page.wait_for_selector('.suggestion', timeout=8000)
            print('Found suggestions')
            book_buttons = page.query_selector_all('.suggestion .s-actions button')
            time.sleep(1)
            # Click the first 'Book' button
            print('book_buttons count', len(book_buttons))
            if book_buttons and len(book_buttons) > 0:
                # second button is 'Book' (Select then Book)
                book_button = book_buttons[1]
                print('Clicking book for first hotel')
                book_button.click()
                print('Clicked book button')
                # Wait for modal and fill
                page.wait_for_selector('#booking-modal', timeout=2000)
                page.fill('#b-name', 'Automation Tester')
                page.fill('#b-phone', '+919000000000')
                # set checkin date to two days from today
                import datetime
                d = datetime.date.today() + datetime.timedelta(days=2)
                page.fill('#b-date', d.isoformat())
                page.fill('#b-nights', '2')
                page.click('#b-confirm')
                print('Clicked confirm button')
                # Wait for booking confirmation from server
                try:
                    page.wait_for_selector('div.msg.bot >> text=Booking confirmed', timeout=10000)
                    print('Booking confirmed message detected')
                except Exception:
                    print('Booking confirmation message not detected explicitly; capturing snapshot anyway')
            else:
                print('No Book buttons found')
        except Exception as e:
            print('Error interacting with UI:', e)
            import traceback
            traceback.print_exc()

        # Wait for UI to finish updating
        time.sleep(1.5)

        # Save screenshot of the chat window area
        # Find element bounding box of #chat-window and screenshot that region
        box = page.query_selector('#chat-window').bounding_box()
        print('Found box:', box)
        screenshot_path = os.path.join(OUT_DIR, 'ui_chat_screenshot.png')
        print('box:', box)
        if box:
            page.screenshot(path=screenshot_path, clip={
                'x': box['x'], 'y': box['y'], 'width': box['width'], 'height': box['height']
            })
        else:
            page.screenshot(path=screenshot_path, full_page=True)

        # Save HTML snapshot of the chat content
        html_path = os.path.join(OUT_DIR, 'ui_chat_snapshot.html')
        html_content = page.eval_on_selector('#chat-body', 'el => el.innerHTML')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print('Saved screenshot to', screenshot_path)
        print('Saved HTML snapshot to', html_path)
        browser.close()

if __name__ == '__main__':
    run()
