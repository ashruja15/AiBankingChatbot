#!/usr/bin/env python3
"""
Complete UI Integration Test
Verifies that the recommendations panel is properly connected and working
"""

import requests
import json
import time
from urllib.parse import urljoin

BASE_URL = 'http://127.0.0.1:5000'

def test_step(step_num, description):
    print(f"\n[STEP {step_num}] {description}")
    print("-" * 70)

def test_api_endpoints():
    """Test all API endpoints"""
    test_step(1, "Verifying all API endpoints")
    
    endpoints = [
        ('GET', '/api/greeting', None),
        ('GET', '/api/dataset', None),
        ('GET', '/api/profile', None),
        ('GET', '/api/recommendations', None),
        ('POST', '/api/chat', {'message': 'hello'}),
    ]
    
    for method, endpoint, payload in endpoints:
        try:
            url = urljoin(BASE_URL, endpoint)
            if method == 'GET':
                r = requests.get(url)
            else:
                r = requests.post(url, json=payload)
            
            status = "✅" if r.ok else "❌"
            print(f"  {status} {method:4} {endpoint:20} → {r.status_code}")
            
            if not r.ok:
                print(f"     ERROR: {r.text[:100]}")
        except Exception as e:
            print(f"  ❌ {method:4} {endpoint:20} → ERROR: {e}")

def test_question_tracking():
    """Test that questions are being tracked for recommendations"""
    test_step(2, "Testing question tracking and recommendations")
    
    test_questions = [
        "What are savings accounts?",
        "How can I get a personal loan?",
        "What credit cards do you offer?",
        "How does mobile banking work?",
        "How is my data secure?",
    ]
    
    try:
        for i, question in enumerate(test_questions, 1):
            response = requests.post(
                urljoin(BASE_URL, '/api/chat'),
                json={'message': question}
            )
            if response.ok:
                data = response.json()
                print(f"  ✅ Question {i}: {question[:40]}...")
                print(f"     Answer score: {data.get('score', 'N/A')}")
            else:
                print(f"  ❌ Question {i} failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error tracking questions: {e}")

def test_profile_state():
    """Check the user interest profile"""
    test_step(3, "Checking user interest profile")
    
    try:
        r = requests.get(urljoin(BASE_URL, '/api/profile'))
        if r.ok:
            profile = r.json()
            print(f"  ✅ Profile retrieved")
            print(f"     Total questions: {profile.get('questions', 0)}")
            print(f"     Top interest: {profile.get('top_interest', 'None')}")
            print(f"     Interests tracked: {len(profile.get('interests', []))}")
            
            interests = profile.get('interests', [])
            for category, score in interests.items():
                print(f"       • {category}: {score:.1f}")
        else:
            print(f"  ❌ Failed to get profile: {r.status_code}")
    except Exception as e:
        print(f"  ❌ Error getting profile: {e}")

def test_recommendations():
    """Test recommendations generation"""
    test_step(4, "Testing recommendations generation")
    
    try:
        r = requests.get(urljoin(BASE_URL, '/api/recommendations'))
        if r.ok:
            data = r.json()
            recs = data.get('recommendations', [])
            print(f"  ✅ Recommendations retrieved: {len(recs)} items")
            
            for i, rec in enumerate(recs, 1):
                print(f"\n     Recommendation {i}:")
                print(f"       Title: {rec.get('title', 'N/A')}")
                print(f"       Desc: {rec.get('description', 'N/A')[:50]}...")
                print(f"       Action: {rec.get('action', 'Learn More')}")
        else:
            print(f"  ❌ Failed to get recommendations: {r.status_code}")
    except Exception as e:
        print(f"  ❌ Error getting recommendations: {e}")

def test_html_file():
    """Check if the main HTML file is being served"""
    test_step(5, "Verifying HTML file is served")
    
    try:
        r = requests.get(BASE_URL)
        if r.ok:
            html = r.text
            checks = [
                ('recommendations section', 'id="recommendations"'),
                ('showRecommendations function', 'function showRecommendations'),
                ('rec-items div', 'id="recItems"'),
                ('rec-header element', 'class="rec-header"'),
                ('CSS grid layout', 'grid-template-rows: auto auto 1fr auto auto'),
            ]
            
            print(f"  ✅ HTML file served (size: {len(html)} bytes)")
            print(f"\n     Checking for key elements:")
            
            for check_name, check_string in checks:
                found = "✅" if check_string in html else "❌"
                print(f"       {found} {check_name}")
        else:
            print(f"  ❌ Failed to get HTML: {r.status_code}")
    except Exception as e:
        print(f"  ❌ Error verifying HTML: {e}")

def main():
    print("=" * 70)
    print("UI INTEGRATION VERIFICATION TEST")
    print("=" * 70)
    
    try:
        # Check if server is running
        print("\nChecking server connectivity...")
        r = requests.get(BASE_URL, timeout=2)
        print("✅ Server is running at http://127.0.0.1:5000")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Server is not running!")
        print("   Start the server with: python -m ai_banking_chatbot.server")
        return
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return
    
    # Run tests
    test_api_endpoints()
    test_question_tracking()
    test_profile_state()
    test_recommendations()
    test_html_file()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    If all steps show ✅, the recommendations feature is fully integrated:
    
    1. Visit http://127.0.0.1:5000 in your browser
    2. Ask a banking question (e.g., "What are savings accounts?")
    3. The "💡 Personalized for You" panel should appear below the chat
    4. Ask more questions to see recommendations update
    
    TROUBLESHOOTING:
    • If panel doesn't show: Hard refresh (Ctrl+F5) and try again
    • Clear browser cache: Ctrl+Shift+Delete
    • Check browser console (F12) for JavaScript errors
    • Make sure server is running: netstat -ano | findstr :5000
    """)

if __name__ == '__main__':
    main()
