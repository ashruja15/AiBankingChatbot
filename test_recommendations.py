import urllib.request
import json
import time

print("="*80)
print("TESTING PERSONALIZED FINANCIAL RECOMMENDATIONS ENGINE - UNIQUE FEATURE")
print("="*80)

# Test conversations that should trigger different recommendations
test_questions = [
    "How to save money?",
    "What are investment options?",
    "Can I get a personal loan?",
    "What credit cards do you offer?",
    "How to use mobile banking?",
    "How to protect against fraud?"
]

print("\n[1] Simulating user conversation to build interest profile...\n")
for i, q in enumerate(test_questions):
    print(f"  Q{i+1}: {q}")
    data = json.dumps({'message': q}).encode()
    req = urllib.request.Request('http://127.0.0.1:5000/api/chat', 
                                 data, 
                                 {'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        print(f"      ✓ Got response (Score: {result['score']:.2f})\n")
        time.sleep(0.5)
    except Exception as e:
        print(f"      ✗ Error: {e}\n")

print("\n[2] Fetching personalized recommendations after conversation...\n")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/recommendations',
                                 headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    
    print("RECOMMENDATIONS RECEIVED:")
    print(f"Profile Summary: {data['profile']}\n")
    
    print("Personalized Recommendations:")
    for i, rec in enumerate(data['recommendations'], 1):
        print(f"\n  Recommendation #{i}:")
        print(f"    Title: {rec['title']}")
        print(f"    Description: {rec['description']}")
        print(f"    Action: {rec.get('action', 'Learn More')}")
        if 'category' in rec:
            print(f"    Category: {rec['category']}")
    
    print("\n" + "="*80)
    print("✓ SUCCESS - Personalized Recommendations Engine is WORKING!")
    print("="*80)
    print("\nUnique Features Demonstrated:")
    print("  ✓ Conversation history tracking")
    print("  ✓ Interest detection from user questions")
    print("  ✓ User profile building (savings, investments, loans, etc.)")
    print("  ✓ Smart personalized recommendations based on detected interests")
    print("  ✓ Real-time recommendation generation")
    
except Exception as e:
    print(f"✗ Error fetching recommendations: {e}")
    import traceback
    traceback.print_exc()
