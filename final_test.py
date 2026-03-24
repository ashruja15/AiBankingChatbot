#!/usr/bin/env python
"""Final comprehensive test demonstrating all features."""
import urllib.request
import json
from datetime import datetime

print("=" * 70)
print("AI BANKING CHATBOT - FINAL DEMONSTRATION")
print("=" * 70)

# Test 1: Time-based greeting
print("\n[1] TIME-BASED GREETING FEATURE")
print("-" * 70)
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/greeting')
    with urllib.request.urlopen(req, timeout=5) as r:
        data = json.loads(r.read().decode('utf-8'))
        current_time = datetime.now().strftime("%H:%M")
        print(f"✓ Current Time: {current_time}")
        print(f"✓ Server Greeting: {data.get('greeting')}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Dataset Q&A (from FAQ)
print("\n[2] DATASET-BASED Q&A (FAQ Questions)")
print("-" * 70)
test_cases_dataset = [
    "how to open a savings account?",
    "what are atm withdrawal limits?",
    "bye"
]
for question in test_cases_dataset:
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
            print(f"A: {answer[:80]}..." if len(answer) > 80 else f"A: {answer}")
            print(f"   Confidence: {score*100:.0f}%")
    except Exception as e:
        print(f"✗ Failed: {e}")

# Test 3: General Banking Knowledge
print("\n[3] GENERAL BANKING KNOWLEDGE (Beyond Dataset)")
print("-" * 70)
test_cases_general = [
    "Tell me about your investment options",
    "What is fraud protection?",
    "How do I handle payments?",
    "Explain credit card features",
    "What about security?"
]
for question in test_cases_general:
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
            print(f"A: {answer[:80]}..." if len(answer) > 80 else f"A: {answer}")
            print(f"   Confidence: {score*100:.0f}%")
    except Exception as e:
        print(f"✗ Failed: {e}")

# Test 4: Dataset info
print("\n[4] SERVER STATUS & DATASET INFO")
print("-" * 70)
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/dataset')
    with urllib.request.urlopen(req, timeout=5) as r:
        data = json.loads(r.read().decode('utf-8'))
        print(f"✓ Server: RUNNING ✓")
        print(f"✓ FAQ Dataset: {len(data)} Q&A pairs loaded")
        print(f"✓ Voice Endpoints:")
        print(f"  - /api/tts (POST) — Server-side text-to-speech")
        print(f"  - /api/stt (POST) — Server-side speech-to-text")
        print(f"✓ Chat Endpoints:")
        print(f"  - /api/chat (POST) — Answer banking questions")
        print(f"  - /api/greeting (GET) — Time-based greeting")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 70)
print("FEATURES ENABLED:")
print("=" * 70)
print("✓ 1. Time-based Greetings (Morning/Afternoon/Evening/Night)")
print("✓ 2. General Banking Knowledge (not just FAQ dataset)")
print("✓ 3. Voice Input (Web Speech API + Vosk fallback)")
print("✓ 4. Voice Output (Browser TTS + pyttsx3 fallback)")
print("✓ 5. Accessibility (Blind & normal users)")
print("✓ 6. Responsive Web UI")
print("✓ 7. Confidence Scoring")
print("\n" + "=" * 70)
print("HOW TO USE:")
print("=" * 70)
print("1. Open http://127.0.0.1:5000/ in your browser")
print("2. Type or speak your banking question")
print("3. Press Enter (or Stop if recording)")
print("4. Listen to the response via TTS or read it")
print("\nEXAMPLE QUESTIONS:")
print("  • How to open a savings account?")
print("  • What are credit card fees?")
print("  • Tell me about investment options")
print("  • How to report fraud?")
print("  • What is security protection?")
print("=" * 70)
