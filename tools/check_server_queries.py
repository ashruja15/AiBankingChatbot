from ai_banking_chatbot import server as s
client = s.app.test_client()
queries = ['hello', 'what is overdraft fee', 'how do i open a new bank account?', 'what is my account balance?']
for q in queries:
    r = client.post('/api/chat', json={'message': q})
    print(q, '->', r.status_code, r.get_json())
