#!/usr/bin/env python
"""Test time-based greetings and general banking knowledge."""
import urllib.request
import json

def test_greeting():
    """Test the /api/greeting endpoint."""
    url = 'http://127.0.0.1:5000/api/greeting'
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print(f'✓ GET {url} -> {r.status}')
            data = json.loads(r.read().decode('utf-8'))
            print(f'  Greeting: {data.get("greeting")}')
    except Exception as e:
        print(f'✗ GET {url} failed: {e}')

def test_general_banking_question(question):
    """Test handling general banking questions."""
    url = 'http://127.0.0.1:5000/api/chat'
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps({'message': question}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f'✓ Question: "{question}"')
            print(f'  Answer: {data.get("answer")}')
            print(f'  Score: {data.get("score")}')
    except Exception as e:
        print(f'✗ POST {url} failed: {e}')

if __name__ == '__main__':
    print('=== Testing Time-based Greeting ===')
    test_greeting()
    
    print('\n=== Testing General Banking Questions ===')
    test_general_banking_question('how do I invest money?')
    test_general_banking_question('what are credit card fees?')
    test_general_banking_question('how to get a home loan?')
    test_general_banking_question('tell me about your investment options')
    test_general_banking_question('what is fraud protection?')
