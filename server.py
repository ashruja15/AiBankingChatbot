import http.server
import socketserver
import json
import os
import tempfile
import wave
import traceback
from urllib.parse import urlparse, parse_qs

try:
    from ai_banking_chatbot.chatbot import load_dataset, find_best_answer, DATASET_PATH, get_time_based_greeting, UserInterestProfile
except Exception:
    from chatbot import load_dataset, find_best_answer, DATASET_PATH, get_time_based_greeting, UserInterestProfile

PORT = 5000
ROOT = os.path.dirname(__file__)
STATIC_DIR = ROOT

# Initialize global user profile for personalized recommendations
user_profile = UserInterestProfile()

# Optional speech libraries (import lazily where used)
VOSK_MODEL = None
VOSK_MODEL_PATH = os.path.join(ROOT, 'models', 'vosk-model-small-en-us-0.15')
try:
    from vosk import Model
    if os.path.exists(VOSK_MODEL_PATH):
        try:
            VOSK_MODEL = Model(VOSK_MODEL_PATH)
        except Exception:
            VOSK_MODEL = None
except Exception:
    VOSK_MODEL = None

# Serve static files from the package directory
os.chdir(STATIC_DIR)

# Load knowledge base using an absolute path so dataset is found
kb = load_dataset(os.path.join(ROOT, DATASET_PATH))

class ChatbotHandler(http.server.SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        """Add CORS headers to allow cross-origin requests"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Serve index.html
        if path == "/":
            self.path = "/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        # Serve time-based greeting
        elif path == "/api/greeting":
            greeting = get_time_based_greeting()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"greeting": greeting}).encode("utf-8"))
            return

        # Serve dataset JSON
        elif path == "/api/dataset":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(kb).encode("utf-8"))
            return

        # Personalized Recommendations API - UNIQUE FEATURE
        elif path == "/api/recommendations":
            recommendations = user_profile.get_recommendations(limit=3)
            profile = user_profile.get_profile_summary()
            response = {
                "recommendations": recommendations,
                "profile": profile
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # User Profile API
        elif path == "/api/profile":
            profile = user_profile.get_profile_summary()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(profile).encode("utf-8"))
            return

        # Serve static files
        else:
            # Serve files from STATIC_DIR
            if os.path.exists(STATIC_DIR + path):
                self.path = path
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.send_error(404, "File not found")
                return

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # Server-side TTS endpoint: returns WAV audio bytes for the given text
        if path == "/api/tts":
            text = data.get('text', '') if isinstance(data, dict) else ''
            if not text:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "empty text"}).encode("utf-8"))
                return
            try:
                import pyttsx3
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                tmp.close()
                engine = pyttsx3.init()
                engine.save_to_file(text, tmp.name)
                engine.runAndWait()
                with open(tmp.name, 'rb') as f:
                    audio = f.read()
                try:
                    os.unlink(tmp.name)
                except Exception:
                    pass
                self.send_response(200)
                self.send_header("Content-type", "audio/wav")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(audio)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "TTS failed", "detail": str(e)}).encode("utf-8"))
            return

        # Server-side STT endpoint: accept raw WAV bytes in body and attempt to transcribe with Vosk
        if path == "/api/stt":
            # If body is empty, bad request
            if not body:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "empty audio body"}).encode('utf-8'))
                return
            tmp = None
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                tmp.write(body)
                tmp.close()
                if VOSK_MODEL is None:
                    # Model not loaded or vosk not installed
                    raise RuntimeError('Vosk model not available on server')
                from vosk import KaldiRecognizer
                wf = wave.open(tmp.name, "rb")
                rec = KaldiRecognizer(VOSK_MODEL, wf.getframerate())
                results = []
                while True:
                    data_chunk = wf.readframes(4000)
                    if len(data_chunk) == 0:
                        break
                    if rec.AcceptWaveform(data_chunk):
                        results.append(rec.Result())
                results.append(rec.FinalResult())
                wf.close()
                # extract text parts
                import ast
                text = ' '.join([ast.literal_eval(r).get('text', '') if r and r.startswith('{') else '' for r in results]).strip()
                try:
                    os.unlink(tmp.name)
                except Exception:
                    pass
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"text": text}).encode('utf-8'))
                return
            except Exception as e:
                if tmp:
                    try: os.unlink(tmp.name)
                    except Exception: pass
                self.send_response(501 if isinstance(e, RuntimeError) else 500)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "STT failed", "detail": str(e)}).encode('utf-8'))
                return

        # Chat API with personalized recommendations tracking
        if path == "/api/chat":
            msg = data.get("message", "")
            if not msg:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "empty message"}).encode("utf-8"))
                return

            # Track question for personalized recommendations
            user_profile.track_question(msg)
            
            answer, score = find_best_answer(msg, kb)
            response = {"answer": answer, "score": score, "question": None if score==0 else msg}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        else:
            self.send_error(404, "API endpoint not found")
            return

class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

with ThreadingHTTPServer(("", PORT), ChatbotHandler) as httpd:
    print(f"Serving on http://127.0.0.1:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
