import urllib.request
import json

print("Debugging Personalized Recommendations Feature\n")
print("="*80)

# Test 1: Check if server is responding
print("\n[Test 1] Server connectivity...")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/greeting')
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✓ Server is responding. Greeting: {data['greeting'][:50]}...")
except Exception as e:
    print(f"✗ Server error: {e}")
    exit(1)

# Test 2: Check recommendations endpoint WITHOUT any conversation
print("\n[Test 2] Recommendations endpoint (fresh profile)...")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/recommendations')
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✓ Endpoint accessible")
    print(f"  Profile: {data['profile']}")
    print(f"  Recommendations count: {len(data['recommendations'])}")
    if len(data['recommendations']) > 0:
        print(f"  First rec: {data['recommendations'][0]['title']}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Send a chat message and check if it's tracked
print("\n[Test 3] Sending test question to build profile...")
try:
    msg_data = json.dumps({'message': 'How do I invest money?'}).encode()
    req = urllib.request.Request('http://127.0.0.1:5000/api/chat',
                                 msg_data,
                                 {'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✓ Chat response received (score: {data['score']})")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Check recommendations after conversation
print("\n[Test 4] Recommendations after chat message...")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/recommendations')
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✓ Profile updated")
    print(f"  Total questions asked: {data['profile'].get('total_questions', 0)}")
    print(f"  Top interest: {data['profile'].get('top_interest', 'None')}")
    print(f"  All interests: {data['profile'].get('all_interests', {})}")
    print(f"\n  Recommendations generated:")
    for i, rec in enumerate(data['recommendations'], 1):
        print(f"    {i}. {rec['title']}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Check user profile API
print("\n[Test 5] User profile endpoint...")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/profile')
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✓ Profile retrieved: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
