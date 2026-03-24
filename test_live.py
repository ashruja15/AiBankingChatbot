#!/usr/bin/env python
"""Quick test to see what the live server is returning."""
import urllib.request
import json

questions = [
    "what are the requirements for a home loan?",
    "how to get a home loan?",
    "tell me about home loans",
    "how do I invest money?",
    "what about credit card fees?",
]

print("Testing Live Server Responses:\n")
for q in questions:
    try:
        req = urllib.request.Request(
            'http://127.0.0.1:5000/api/chat',
            data=json.dumps({'message': q}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Q: {q}")
            print(f"A: {data.get('answer')}")
            print(f"Score: {data.get('score')}\n")
    except Exception as e:
        print(f"Error: {e}\n")
