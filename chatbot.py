import json
import os
import re
import sys
from difflib import SequenceMatcher

# Simple Banking FAQ Chatbot using fuzzy match over a small Q&A dataset
# No external dependencies; runs with Python 3.8+

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset.json')


def load_dataset(path: str):
    if not os.path.exists(path):
        print(f"Dataset not found at {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize(text: str) -> str:
    # Lowercase, remove non-alphanumeric except spaces
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_best_answer(query: str, kb):
    nq = normalize(query)
    best = (0.0, None)
    # Try exact keyword containment first for quick wins
    for qa in kb:
        qn = normalize(qa['question'])
        if nq in qn or qn in nq:
            return qa['answer'], 1.0
    # Fallback to fuzzy
    for qa in kb:
        qn = normalize(qa['question'])
        score = similarity(nq, qn)
        if score > best[0]:
            best = (score, qa['answer'])
    return best[1], best[0]


def chat_loop(kb):
    print("Banking FAQ Chatbot\nType your question. Type 'help' for tips or 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not user:
            continue
        if user.lower() in {"exit", "quit", "q"}:
            print("Goodbye.")
            break
        if user.lower() in {"help", "?"}:
            print("- Ask simple banking questions like 'How to open a savings account?'")
            print("- Type 'suggest' to see example questions from the dataset.")
            continue
        if user.lower() == "suggest":
            examples = [qa['question'] for qa in kb[:8]]
            print("Try asking:")
            for e in examples:
                print(f"  - {e}")
            continue

        answer, score = find_best_answer(user, kb)
        if answer is None or score < 0.5:
            print("Bot: I'm not sure. Please try rephrasing or type 'suggest' for examples.")
        else:
            print(f"Bot: {answer}")


if __name__ == '__main__':
    kb = load_dataset(DATASET_PATH)
    chat_loop(kb)
