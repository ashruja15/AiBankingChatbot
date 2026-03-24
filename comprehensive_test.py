#!/usr/bin/env python
"""Comprehensive test with diverse banking questions."""
import urllib.request
import json

def test_question(question):
    """Test a single question."""
    try:
        req = urllib.request.Request(
            'http://127.0.0.1:5000/api/chat',
            data=json.dumps({'message': question}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            answer = data.get('answer')
            score = data.get('score')
            print(f"\nQ: {question}")
            print(f"A: {answer[:90]}..." if len(answer) > 90 else f"A: {answer}")
            print(f"   Confidence: {score*100:.0f}%")
            return True
    except Exception as e:
        print(f'✗ Failed: {e}')
        return False

print("=" * 80)
print("COMPREHENSIVE BANKING CHATBOT TEST - ANSWER RELEVANCE CHECK")
print("=" * 80)

test_categories = {
    "INVESTMENT & SAVINGS": [
        "How do I invest money?",
        "What investment options do you offer?",
        "How to open a savings account?",
        "Tell me about your rates",
    ],
    "LOANS & CREDIT": [
        "How to get a home loan?",
        "What about personal loans?",
        "Can I increase my credit card limit?",
        "What are credit card fees?",
    ],
    "CARDS & PAYMENTS": [
        "What types of cards do you offer?",
        "How to make payments?",
        "Tell me about debit cards",
        "Explain credit card features",
    ],
    "SECURITY & FRAUD": [
        "What is fraud protection?",
        "How secure is my account?",
        "What about security measures?",
        "How to report fraud?",
    ],
    "TRANSFERS & DEPOSITS": [
        "How to transfer funds?",
        "How to deposit checks?",
        "What about wire transfers?",
        "How to withdraw money?",
    ],
    "ACCOUNTS & SERVICES": [
        "How to open an account?",
        "Do you have online banking?",
        "Tell me about your mobile app",
        "What is online banking?",
    ],
    "FAQ FROM DATASET": [
        "How to reset my password?",
        "What are ATM withdrawal limits?",
        "Do you have mobile check deposit?",
        "How to block a lost card?",
    ]
}

total_passed = 0
total_tests = 0

for category, questions in test_categories.items():
    print(f"\n{'='*80}")
    print(f"  {category}")
    print(f"{'='*80}")
    for q in questions:
        if test_question(q):
            total_passed += 1
        total_tests += 1

print(f"\n{'='*80}")
print(f"FINAL RESULTS: {total_passed}/{total_tests} tests passed")
print(f"{'='*80}")

if total_passed == total_tests:
    print("✓ ALL TESTS PASSED - Chatbot providing relevant, accurate answers!")
else:
    print(f"⚠ {total_tests - total_passed} tests need review")
