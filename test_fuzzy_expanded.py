import urllib.request
import json

variants = [
    'tell me about banks',
    'saving accounts vs checking accounts',
    'how does FD work?',
    'explain interest',
    'what is KYC verification?',
    'how to use ATM?',
    'loan basics',
    'what does EMI mean?',
    'central bank of India',
    'fund transfers NEFT',
    'credit card vs debit card',
    'home loans explained',
    'what is UPI?',
    'online banking services',
    'NPA meaning'
]

print("Testing Fuzzy Matching with Expanded Dataset:\n")
for q in variants:
    data = json.dumps({'message': q}).encode()
    req = urllib.request.Request('http://127.0.0.1:5000/api/chat', data, {'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        ans = result['answer']
        if len(ans) > 70:
            ans = ans[:70] + "..."
        print(f"Q: {q}")
        print(f"A: {ans}")
        print(f"Score: {result['score']:.2f} | Matched: {result['question'][:50]}...\n" if len(result['question']) > 50 else f"Score: {result['score']:.2f} | Matched: {result['question']}\n")
    except Exception as e:
        print(f"Error: {e}\n")
