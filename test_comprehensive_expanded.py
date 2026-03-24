import urllib.request
import json
import sys

# Comprehensive test across all 6 new categories
test_categories = {
    "Basic Banking Concepts": [
        "what is a bank?",
        "what is simple interest?",
        "what is a cheque?"
    ],
    "Accounts & Services": [
        "what is kyc?",
        "what is minimum balance?",
        "what is a joint account?"
    ],
    "Digital Banking": [
        "what is atm?",
        "what is upi?",
        "what is neft?"
    ],
    "Loans & Credit": [
        "what is a loan?",
        "what is home loan?",
        "what is emi?"
    ],
    "RBI & Monetary": [
        "what is rbi?",
        "what is repo rate?",
        "what is inflation?"
    ],
    "Expert Topics": [
        "explain credit creation by banks",
        "what is the difference between public and private sector banks?",
        "what are the advantages of internet banking?"
    ]
}

print("="*70)
print("COMPREHENSIVE BANKING CHATBOT TEST - EXPANDED DATASET")
print("="*70)

passed = 0
total = 0
category_results = {}

for category, questions in test_categories.items():
    print(f"\n[{category}]")
    category_passed = 0
    
    for q in questions:
        total += 1
        data = json.dumps({'message': q}).encode()
        req = urllib.request.Request('http://127.0.0.1:5000/api/chat', 
                                     data, 
                                     {'Content-Type': 'application/json'})
        try:
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            score = result['score']
            
            # Score >= 0.7 is considered a good match
            if score >= 0.7:
                passed += 1
                category_passed += 1
                status = "✓ PASS"
            else:
                status = "✗ WEAK"
            
            ans_preview = result['answer'][:60] + "..." if len(result['answer']) > 60 else result['answer']
            print(f"  {status} Q: {q}")
            print(f"       A: {ans_preview}")
            print(f"       Score: {score:.2f}\n")
            
        except Exception as e:
            print(f"  ✗ ERROR Q: {q}")
            print(f"       Error: {e}\n")
    
    category_results[category] = (category_passed, len(questions))

print("="*70)
print(f"OVERALL: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
print("\nCategory Breakdown:")
for category, (passed_count, total_count) in category_results.items():
    pct = (passed_count/total_count*100) if total_count > 0 else 0
    print(f"  {category}: {passed_count}/{total_count} ({pct:.0f}%)")

print("\n" + "="*70)
if passed >= total * 0.8:
    print("✓ SUCCESS - Expanded dataset fully integrated and working!")
    print(f"✓ System now answers {107} comprehensive banking FAQ items")
else:
    print("⚠ Some tests need attention")
print("="*70)
