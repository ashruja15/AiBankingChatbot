import requests

test_questions = ['hello', 'how to open a savings account', 'what is a bank', 'random gibberish question']

for q in test_questions:
    r = requests.post('http://localhost:5000/api/chat', json={'message': q})
    result = r.json()
    print(f'Q: {q}')
    print(f'  Score: {result["score"]} - Answer: {result["answer"][:60]}...')
    print()
