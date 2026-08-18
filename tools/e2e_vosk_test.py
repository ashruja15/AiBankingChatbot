"""End-to-end Vosk transcription test.

This script:
 - Synthesizes a short WAV using pyttsx3 (text: 'what is overdraft fee')
 - Loads an installed Vosk model from `ai_banking_chatbot/models` (first folder starting with 'vosk-model')
 - Runs KaldiRecognizer on the file and prints a JSON report to stdout

Exit codes:
 - 0: Passed (transcript contains expected keyword)
 - 1: Failed (transcript missing expected keyword)
 - 2: Error (missing deps or unexpected exception)
"""
import json
import sys
from pathlib import Path

EXPECTED_KEYWORD = 'overdraft'
TEST_TEXT = 'what is overdraft fee'
ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / 'models'
SAMPLE_WAV = Path(__file__).resolve().parent / 'sample_vosk_test.wav'

try:
    import pyttsx3
    from vosk import Model, KaldiRecognizer
    import wave
except Exception as e:
    print(json.dumps({'error': 'missing_dependency', 'details': str(e)}))
    sys.exit(2)

# Find a model
models = [p for p in MODELS_DIR.iterdir() if p.is_dir() and p.name.startswith('vosk-model')]
if not models:
    print(json.dumps({'error': 'no_vosk_model', 'details': f'No models in {MODELS_DIR}'}))
    sys.exit(2)
model_path = str(models[0])

# Synthesize speech to file
try:
    engine = pyttsx3.init()
    engine.save_to_file(TEST_TEXT, str(SAMPLE_WAV))
    engine.runAndWait()
except Exception as e:
    print(json.dumps({'error': 'tts_failed', 'details': str(e)}))
    sys.exit(2)

# Run Vosk on the file
try:
    wf = wave.open(str(SAMPLE_WAV), 'rb')
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    transcript = ''
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            transcript += ' ' + res.get('text', '')
    final = json.loads(rec.FinalResult())
    transcript += ' ' + final.get('text', '')
    transcript = transcript.strip()
except Exception as e:
    print(json.dumps({'error': 'vosk_failed', 'details': str(e)}))
    sys.exit(2)
finally:
    try:
        wf.close()
    except Exception:
        pass

report = {'transcript': transcript}
if EXPECTED_KEYWORD in transcript.lower():
    report['ok'] = True
    print(json.dumps(report))
    sys.exit(0)
else:
    report['ok'] = False
    print(json.dumps(report))
    sys.exit(1)
