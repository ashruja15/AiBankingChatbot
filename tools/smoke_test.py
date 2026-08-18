import json
import sys
from pathlib import Path

# Ensure package import path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from chatbot import reload_optionals, check_dependencies
except Exception as e:
    print(json.dumps({"error": "failed to import chatbot module", "details": str(e)}))
    sys.exit(2)

try:
    reload_optionals()
    checks = check_dependencies()
    report = {
        "speech_recognition": bool(checks.get('speech_recognition')),
        "pyttsx3": bool(checks.get('pyttsx3')),
        "pyaudio": bool(checks.get('pyaudio')),
        "vosk": bool(checks.get('vosk')),
        "microphones": checks.get('microphones', []),
    }
    report['ok'] = report['speech_recognition'] or report['pyttsx3']
    print(json.dumps(report))
    if report['ok']:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(json.dumps({"error": "smoke test failed", "details": str(e)}))
    sys.exit(2)
