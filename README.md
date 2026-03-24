# Banking FAQ Chatbot

Simple command-line banking FAQ chatbot with optional voice input/output.

## Features
- Text-based question/answer chatbot using `dataset.json` (keyword + similarity matching)
- Optional voice input (Speech-to-Text) via `SpeechRecognition`
- Optional Text-to-Speech via `pyttsx3`
- Helpful dependency checks and a `--smoke-test` mode to validate audio components

## Installation (Windows)
1. Create a virtual environment (recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Install core Python packages:
   ```powershell
   pip install -r requirements.txt
   ```
3. On Windows, installing `PyAudio` may require `pipwin` if `pip install PyAudio` fails:
   ```powershell
   pip install pipwin
   pipwin install pyaudio
   ```

## Running
- Text-only:
  ```powershell
  python chatbot.py
  ```
- Try voice support (best-effort):
  ```powershell
  python chatbot.py --voice
  ```
- Run the web UI (serves `index.html` and a simple chat API):
  ```powershell
  # install Flask if not already
  python -m pip install Flask Flask-Cors
  # then run the server
  python -m ai_banking_chatbot.server
  # open http://127.0.0.1:5000 in the browser
  ```

- Run a smoke test to verify microphone and TTS:
  ```powershell
  python chatbot.py --smoke-test
  ```
- Attempt to auto-install missing dependencies:
  ```powershell
  python chatbot.py --install-deps  # will prompt before installing
  python chatbot.py --install-deps --yes  # assume yes
  ```

## Voice troubleshooting
- Microphone not found: check Windows Input devices and privacy settings.
- If `SpeechRecognition` can't use Google (offline), consider offline STT like Vosk.
  - Download a Vosk model (e.g., `https://alphacephei.com/vosk/models`) and point `--vosk-model` to the model directory.
  - This project supports a helper to download and extract a model: `python chatbot.py --download-vosk <model_url>` (you will be prompted before a potentially large download).
- If `pyttsx3` errors: try different TTS engine backends or ensure proper sound drivers.

## Next improvements
- Add full offline STT (Vosk) integration and automatic model download.
- Add a web UI with push-to-talk support.

---

## CI / Automated smoke test ✅
You can run a CI-friendly smoke test to validate that audio/TTS dependencies and microphones are available.

- Run locally (prints human-readable summary):

```powershell
python ai_banking_chatbot/chatbot.py --smoke-test
```

- Run the CI-friendly JSON smoke test (recommended for GitHub Actions):

```powershell
python -m ai_banking_chatbot.tools.smoke_test
```

The script prints a JSON object to stdout. Exit codes:
- `0` : OK (at least one of STT or TTS available)
- `1` : Missing STT and TTS (CI should consider this a failure)
- `2` : Unexpected error while checking

Example GitHub Actions step (Linux runner):

```yaml
- name: Run smoke test
  run: python -m ai_banking_chatbot.tools.smoke_test
```

### Fast setup (install optional voice deps and download a small Vosk model)

A helper script automates installing optional voice-related packages and can download a small English Vosk model for offline STT.

- Non-interactive install + model download (prompts suppressed with `--yes`):

```powershell
python -m ai_banking_chatbot.tools.fast_setup --yes
```

- Dry-run to see actions without performing them:

```powershell
python -m ai_banking_chatbot.tools.fast_setup --dry-run
```

- Skip model download:

```powershell
python -m ai_banking_chatbot.tools.fast_setup --yes --no-model
```

If you want, I can also add a GitHub Actions step to call this fast-setup script in CI or a convenience `make` target.

If you want, I can add a sample workflow file that runs the smoke test on every push.

