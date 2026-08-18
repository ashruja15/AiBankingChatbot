import json
import time
from playwright.sync_api import sync_playwright, TimeoutError

URL = 'http://127.0.0.1:5000/'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)
    # Wait for load and dataset status
    try:
        page.wait_for_selector('#datasetStatus', timeout=5000)
    except TimeoutError:
        print(json.dumps({'error': 'dataset_status_missing'}))
        browser.close()
        raise SystemExit(1)

    # Send a message present in dataset
    page.fill('#input', 'hello')
    # Intercept responses to /api/tts
    tts_info = {'called': False, 'status': None, 'content_type': None}

    def on_response(resp):
        if '/api/tts' in resp.url:
            tts_info['called'] = True
            tts_info['status'] = resp.status
            tts_info['content_type'] = resp.headers.get('content-type')

    page.on('response', on_response)

    page.click('#btnSend')

    # Wait for a bot bubble that is not 'typing…'
    try:
        page.wait_for_function("() => Array.from(document.querySelectorAll('.msg.bot .bubble')).some(b=>b.textContent && !b.textContent.includes('typing'))", timeout=5000)
    except TimeoutError:
        print(json.dumps({'error': 'no_bot_reply'}))
        browser.close()
        raise SystemExit(1)

    bubbles = page.query_selector_all('.msg.bot .bubble')
    bot_text = bubbles[-1].text_content().strip() if bubbles else ''

    # Try server TTS playback by clicking the button if visible
    try:
        btn = page.query_selector('#btnPlayServer')
        if btn and btn.is_visible():
            btn.click()
            # wait for response intercept
            time.sleep(1.5)
    except Exception as e:
        print(json.dumps({'warning': 'play_server_failed', 'details': str(e)}))

    browser.close()
    print(json.dumps({'bot_text': bot_text, 'tts': tts_info}))
