import json
import os
import re
from difflib import SequenceMatcher
from datetime import datetime
from collections import defaultdict

DATASET_PATH = "dataset.json"

# ============================================================================
# PERSONALIZED FINANCIAL RECOMMENDATIONS ENGINE - UNIQUE FEATURE
# ============================================================================
class UserInterestProfile:
    """Tracks user's banking interests and generates personalized recommendations."""
    
    def __init__(self):
        self.interest_scores = defaultdict(float)
        self.questions_asked = []
        self.keywords_detected = defaultdict(int)
        
        # Define interest categories and their associated keywords
        self.interest_categories = {
            'savings': ['savings', 'save', 'interest', 'rate', 'deposit', 'fd', 'fixed'],
            'investments': ['invest', 'investment', 'mutual', 'bond', 'stock', 'portfolio'],
            'loans': ['loan', 'borrow', 'credit', 'emi', 'repay', 'mortgage', 'home loan'],
            'credit': ['credit', 'card', 'limit', 'payment', 'debt', 'score'],
            'digital': ['atm', 'online', 'mobile', 'app', 'transfer', 'upi', 'payment', 'banking'],
            'security': ['fraud', 'security', 'safe', 'protection', 'scam', 'verification', 'kyc'],
            'accounts': ['account', 'open', 'balance', 'minimum', 'joint', 'zero-balance'],
        }
        
        # Recommendations mapped to interest categories
        self.recommendations_map = {
            'savings': {
                'title': 'High-Yield Savings Account',
                'description': 'Based on your interest in savings, we recommend our High-Yield Savings Account offering up to 4.5% APY.',
                'action': 'Open Account',
                'score': 0
            },
            'investments': {
                'title': 'Investment Advisory Service',
                'description': 'Your questions suggest interest in investing. Our certified advisors can help create a diversified portfolio tailored to your goals.',
                'action': 'Schedule Consultation',
                'score': 0
            },
            'loans': {
                'title': 'Personal Loan Pre-Approval',
                'description': 'We can pre-approve you for a personal loan with competitive rates based on your creditworthiness.',
                'action': 'Check Eligibility',
                'score': 0
            },
            'credit': {
                'title': 'Premium Credit Card',
                'description': 'Your spending patterns suggest you\'d benefit from our rewards credit card with cashback and travel perks.',
                'action': 'Apply Now',
                'score': 0
            },
            'digital': {
                'title': 'Mobile Banking Setup',
                'description': 'Simplify your banking with our comprehensive mobile app featuring instant transfers, bill pay, and account management.',
                'action': 'Download App',
                'score': 0
            },
            'security': {
                'title': 'Enhanced Security Package',
                'description': 'Protect your account with our premium security features including 2FA, transaction alerts, and fraud insurance.',
                'action': 'Enable Now',
                'score': 0
            },
            'accounts': {
                'title': 'Account Optimization Review',
                'description': 'Based on your needs, we recommend reviewing your current account type to maximize benefits and minimize fees.',
                'action': 'Learn More',
                'score': 0
            }
        }
    
    def track_question(self, question: str):
        """Track user's question and update interest profile."""
        import re
        self.questions_asked.append(question)
        q_lower = question.lower()
        
        # Detect interests from the question using word boundaries to avoid false matches
        categories_found = set()
        for category, keywords in self.interest_categories.items():
            for keyword in keywords:
                # Use word boundaries to match whole words/phrases only
                if re.search(r'\b' + re.escape(keyword) + r'\b', q_lower):
                    self.keywords_detected[category] += 1
                    if category not in categories_found:
                        self.interest_scores[category] += 1.0
                        categories_found.add(category)
    
    def get_recommendations(self, limit: int = 3) -> list:
        """Generate personalized recommendations based on user profile."""
        if not self.interest_scores:
            # Return default recommendations if no interest detected yet
            return [
                {
                    'title': 'Complete Your Banking Profile',
                    'description': 'Help us customize your banking experience. Answer a few quick questions about your financial goals.',
                    'action': 'Get Started'
                }
            ]
        
        # Score recommendations based on detected interests
        scored_recs = []
        for category, score in sorted(self.interest_scores.items(), key=lambda x: x[1], reverse=True):
            if category in self.recommendations_map:
                rec = self.recommendations_map[category].copy()
                rec['score'] = score
                rec['category'] = category
                scored_recs.append(rec)
        
        # Return top N recommendations
        return scored_recs[:limit]
    
    def get_profile_summary(self) -> dict:
        """Return a summary of the user's interest profile."""
        if not self.interest_scores:
            return {'status': 'new_user', 'questions_asked': 0}
        
        top_interest = max(self.interest_scores.items(), key=lambda x: x[1])[0] if self.interest_scores else None
        
        return {
            'total_questions': len(self.questions_asked),
            'top_interest': top_interest,
            'all_interests': dict(self.interest_scores),
            'keywords_detected': dict(self.keywords_detected)
        }

# Broader banking knowledge base for general questions not in dataset
# Prioritized by relevance and specificity
GENERAL_BANKING_KB = {
    # Investment and savings
    'invest': 'We offer mutual funds, bonds, stocks, and fixed deposits. Speak with our investment advisor for personalized recommendations. You can also open a savings account to start saving.',
    'investment': 'We offer mutual funds, bonds, stocks, and fixed deposits. Speak with our investment advisor for personalized recommendations. You can also open a savings account to start saving.',
    
    # Loans
    'loan': 'We offer personal loans, home loans, and vehicle loans. Check eligibility on our website or visit a branch to apply. Approval depends on income, credit history, and documentation.',
    
    # Accounts
    'account': 'We offer savings accounts, checking accounts, and investment accounts. Visit our branch or go online to open an account. You\'ll need ID, proof of address, and tax ID.',
    
    # Cards
    'card': 'We offer debit, credit, and prepaid cards. Debit cards access your checking account. Credit cards let you borrow and pay back monthly. Prepaid cards are loaded with funds. Visit a branch or apply online.',
    'debit': 'A debit card draws directly from your checking account. You can use it at ATMs and merchants. Daily withdrawal limits typically range from $500-$1000. Check your account settings.',
    'credit': 'A credit card lets you borrow up to a credit limit and pay it back monthly. You build credit history and earn rewards. Late payments incur fees. Check your terms for rates and fees.',
    
    # Transfers and payments
    'transfer': 'Transfer funds via online banking, mobile app, or at a branch. Domestic transfers usually complete same day. International transfers take 1-3 business days and may have fees. Check current rates.',
    'payment': 'Pay bills online, via mobile app, by phone, or at a branch. Set up automatic bill pay for recurring payments. Auto-pay helps avoid late fees and penalties.',
    
    # Fees and rates
    'fee': 'Account fees vary by account type. Some accounts charge no monthly fee. Others may charge for overdrafts, wire transfers, or low balances. Check your account terms or call support.',
    'rate': 'Interest rates vary by product and market conditions. Savings rates are typically 0.01%-2%. Loan rates depend on credit score and market conditions. Visit our Rates page or call for quotes.',
    'interest': 'Interest is paid on savings accounts and earned on loans you give. Rates vary by account type and market. Check our Rates page for current APY on savings, CDs, and loans.',
    
    # Security and fraud
    'security': 'We use bank-level encryption and 2-factor authentication to protect your account. Never share passwords, PINs, or OTP codes. Report suspicious activity immediately.',
    'fraud': 'Report suspected fraud immediately to us. We investigate and provide provisional credit if needed. Check your statements regularly and enable transaction alerts.',
    'protection': 'We protect your account with encryption, 2FA, and fraud monitoring. Your deposits are FDIC insured up to $250,000. Enable alerts and review statements regularly.',
    
    # Deposits and withdrawals
    'deposit': 'Deposit checks via mobile app (by photo) or at any branch. Mobile deposits typically process within 1-2 business days. You can also transfer funds electronically.',
    'withdraw': 'Withdraw cash at any of our ATMs or visit a branch. Daily ATM limits are typically $500-$1000. Check your account settings or call support for your specific limit.',
    
    # Bills and automated services
    'bill': 'Pay bills through online banking or mobile app. Set up automatic bill pay for utility companies, credit cards, and loans. This saves time and helps avoid late fees.',
    'autopay': 'Automatic bill pay lets you schedule recurring payments. Set up a payee, amount, and date. Payments are deducted from your account automatically. Saves time and avoids late fees.',
    
    # Digital banking
    'online': 'Use our online banking portal or mobile app to check balances, transfer funds, pay bills, and more. It\'s available 24/7. Sign up on our website or download the app.',
    'app': 'Download our mobile app from the App Store or Google Play. Access your account 24/7, deposit checks by photo, get alerts, and manage your finances on the go.',
    'mobile': 'Our mobile app lets you manage your account anytime, anywhere. Check balances, transfer funds, deposit checks (photo), pay bills, and get alerts. Available iOS and Android.',
}

def get_time_based_greeting():
    """Return a greeting based on the current time."""
    now = datetime.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        return "Good morning! How can I help you with your banking today?"
    elif 12 <= hour < 17:
        return "Good afternoon! What banking question can I answer for you?"
    elif 17 <= hour < 21:
        return "Good evening! How can I assist you?"
    else:
        return "It's a bit late, but I'm still here! How can I help with your banking needs?"

def normalize(text: str) -> str:
    """Lowercase, remove punctuation, extra spaces"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_dataset(path: str):
    if not os.path.exists(path):
        print(f"Dataset not found at {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def find_best_answer(user_question: str, dataset):
    """Find the best answer by prioritizing: exact match > general KB > strong fuzzy match > fallback."""
    user_norm = normalize(user_question)

    # 1. Exact match in dataset (highest confidence)
    for qa in dataset:
        if normalize(qa.get("question", "")) == user_norm:
            return qa.get("answer", ""), 1.0

    # 2. Check for general banking KB match (high priority if found)
    general_answer = answer_general_banking_question(user_question)
    
    # 3. Fuzzy matching in dataset
    best_score = 0
    best_answer = ""
    for qa in dataset:
        score = similarity(user_norm, normalize(qa.get("question", "")))
        if score > best_score:
            best_score = score
            best_answer = qa.get("answer", "")

    # Priority order: Exact > General KB (if specific match) > Very strong dataset > General KB (as fallback) > Moderate dataset > Final fallback
    
    # If we found a very strong dataset match, use it
    if best_score >= 0.85:
        return best_answer, round(best_score, 2)
    
    # If we have a specific general banking answer, prefer it over moderate dataset matches
    if general_answer:
        # Use general KB unless dataset is very strong
        if best_score < 0.75:
            return general_answer, 0.85  # High confidence for targeted banking KB answer
    
    # If we have a strong dataset match, use it
    if best_score >= 0.70:
        return best_answer, round(best_score, 2)
    
    # Fallback: use general answer if we have it
    if general_answer:
        return general_answer, 0.85
    
    # Last resort: moderate dataset match
    if best_score >= 0.35:
        return best_answer, round(best_score, 2)
    
    # Final fallback
    return "I'm not sure about that specific question. For detailed banking information, please contact our support team at 1-800-BANK-HELP or visit your nearest branch.", 0

def answer_general_banking_question(question: str) -> str:
    """Answer a general banking question using keyword matching."""
    q_norm = normalize(question).lower()
    
    # Check each keyword in the KB (first match wins, so order matters)
    # Longer keywords first to avoid false matches
    for keyword in sorted(GENERAL_BANKING_KB.keys(), key=len, reverse=True):
        if keyword in q_norm:
            return GENERAL_BANKING_KB[keyword]
    
    # If no keyword found but it's a banking question, provide general guidance
    banking_keywords = ['bank', 'account', 'card', 'money', 'transfer', 'payment', 'loan', 'fee', 'rate', 'deposit', 'withdraw', 'savings', 'credit', 'debit']
    if any(word in q_norm for word in banking_keywords):
        # Provide more helpful generic response
        return "That's a great banking question! Our team is available to help. Please contact us at 1-800-BANK-HELP, visit your nearest branch, or check our website for more information."
    
    return None

def chat_loop(dataset):
    exact_dict = {}
    for qa in dataset:
        q = qa.get('question', '').strip()
        a = qa.get('answer', '').strip()
        if q and a:
            exact_dict[normalize(q)] = a

    print("Banking FAQ Chatbot")
    print("Type your question. Type 'help' for tips, 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower().strip()
        if cmd in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if cmd in {"help", "?"}:
            print("- Ask banking questions like 'how to open a savings account?'")
            print("- Type 'suggest' to see example questions.")
            continue
        if cmd == "suggest":
            print("Try asking:")
            for qa in dataset[:8]:
                print(f"  - {qa['question']}")
            continue

        answer, score = find_best_answer(user_input, dataset)
        print(f"Bot: {answer}")

if __name__ == "__main__":
    dataset = load_dataset(DATASET_PATH)
    chat_loop(dataset)
