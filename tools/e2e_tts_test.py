"""End-to-end test for chat + server-side TTS endpoint.

This script:
 - Uses the Flask app test client to POST /api/chat with a sample message
 - Calls /api/tts with the returned answer and verifies the response is WAV audio

Exit codes:
 - 0: success
 - 1: failed (assertion)
 - 2: error (exception)
"""
import sys
import json
from pathlib import Path

try:
    from ai_banking_chatbot import server as s
except Exception as e:
    print(json.dumps({'error': 'import_failed', 'details': str(e)}))
    sys.exit(2)

client = s.app.test_client()
SAMPLE = 'hello'
try:
    r = client.post('/api/chat', json={'message': SAMPLE})
    if r.status_code != 200:
        print(json.dumps({'error': 'chat_failed', 'status': r.status_code, 'body': r.get_data(as_text=True)}))
        sys.exit(1)
    j = r.get_json() or {}
    answer = j.get('answer')
    if not answer:
        print(json.dumps({'error': 'no_answer', 'details': j}))
        sys.exit(1)
    # Call TTS
    r2 = client.post('/api/tts', json={'text': answer})
    if r2.status_code == 501:
        print(json.dumps({'error': 'tts_unavailable', 'details': r2.get_json()}))
        sys.exit(1)
    if r2.status_code != 200:
        print(json.dumps({'error': 'tts_failed', 'status': r2.status_code, 'body': r2.get_data(as_text=True)}))
        sys.exit(1)
    ctype = r2.headers.get('Content-Type', '')
    data = r2.get_data()
    ok = False
    reason = None
    if ctype.startswith('audio') and len(data) > 44:
        # quick WAV header check for 'RIFF' and 'WAVE'
        if data[:4] == b'RIFF' and b'WAVE' in data[:64]:
            ok = True
        else:
            reason = 'not_wav'
    else:
        reason = f'bad_content_type_or_too_small: ctype={ctype} len={len(data)}'

    out = {'answer': answer, 'tts_ok': ok, 'reason': reason}
    print(json.dumps(out))
    sys.exit(0 if ok else 1)
except Exception as e:
    print(json.dumps({'error': 'exception', 'details': str(e)}))
    sys.exit(2)
