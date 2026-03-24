import urllib.request
import json

tests = [
    'what is a bank?',
    'what is the difference between savings account and current account?',
    'what is a fixed deposit?',
    'what is simple interest?',
    'what is kyc?',
    'what is atm?',
    'what is a loan?',
    'what is emi?',
    'what is rbi?',
    'what is neft?'
]

print("Testing Expanded Dataset:\n")
for q in tests:
    data = json.dumps({'message': q}).encode()
    req = urllib.request.Request('http://127.0.0.1:5000/api/chat', data, {'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        ans = result['answer']
        if len(ans) > 80:
            ans = ans[:80] + "..."
        print(f"Q: {q}")
        print(f"A: {ans}")
        print(f"Score: {result['score']}\n")
    except Exception as e:
        print(f"Error testing '{q}': {e}\n")
