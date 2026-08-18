from ai_banking_chatbot import server as s
print('Imported server module')
print('kb length:', len(s.kb))
client = s.app.test_client()
r = client.post('/api/chat', json={'message':'hello'})
print('POST /api/chat:', r.status_code, r.get_json())
r2 = client.get('/api/dataset')
print('GET /api/dataset:', r2.status_code, len(r2.get_json()) if r2.is_json else 'not json')
