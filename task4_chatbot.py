# ============================================================
#  TASK 4 — BASIC RULE-BASED CHATBOT
#  CodeAlpha Python Internship
#  Concepts: if-elif, functions, loops, I/O
# ============================================================

import random
import re
from datetime import datetime

# ── Knowledge base: keywords → multiple responses ────────────
# Each key is a tuple of trigger words/phrases,
# the value is a list of varied responses (chosen randomly).

RESPONSES = {
    # Greetings
    ("hello", "hi", "hey", "good morning", "good evening", "howdy"): [
        "Hello!  How can I help you?",
        "Hi there! Great to talk to you. What can I do for you?",
        "Hey! I'm here to help. Feel free to ask me anything!",
    ],

    # Well-being
    ("how are you", "how are you doing", "you doing well", "are you ok"): [
        "I'm doing great, thanks for asking!  How about you?",
        "All good on my end! Ready to help you out.",
        "Perfect, thanks! How can I be useful to you?",
    ],

    # Bot name / identity
    ("your name", "what are you called", "who are you", "what is your name"): [
        "My name is CodeBot , your CodeAlpha virtual assistant!",
        "I'm CodeBot, built as part of the CodeAlpha internship program.",
        "I'm CodeBot, a Python chatbot here to help you!",
    ],

    # What the bot can do
    ("what can you do", "your capabilities", "help", "what do you know"): [
        "I can answer your questions, chat with you, and give you basic info! ",
        "I can chat, answer questions, and even tell you the time! Give it a try.",
        "I'm a basic assistant — ask me simple questions and I'll do my best!",
    ],

    # Time / date
    ("time", "what time", "date", "today", "what day"): [
        None,  # dynamic response — handled in get_response()
    ],

    # Weather
    ("weather", "temperature", "is it raining", "forecast"): [
        "I can't access real-time weather, but you can check weather.com! ",
        "For the weather, I'd suggest a dedicated site. I live in the cloud! ",
    ],

    # Joke
    ("joke", "make me laugh", "tell me a joke", "funny"): [
        "Why do programmers prefer dark mode? Because light attracts bugs! ",
        "A Python developer walks into a bar… and orders a snake bite. ",
        "Why did the computer go to the doctor? Because it had a virus! ",
    ],

    # Thanks
    ("thank you", "thanks", "thank you so much", "great", "awesome", "perfect"): [
        "You're welcome! ",
        "Happy to help! Feel free to ask if you have more questions.",
        "My pleasure! ",
    ],

    # Goodbye
    ("goodbye", "bye", "see you", "see you later", "good night", "farewell"): [
        "Goodbye!  Have a wonderful day!",
        "See you later! Don't hesitate to come back if you have questions.",
        "Bye bye!  Take care!",
    ],

    # Python language
    ("python", "programming", "code", "script", "coding"): [
        "Python is a fantastic language!  Simple, powerful, and versatile.",
        "Python programming is at the core of my existence! Need help with a concept?",
        "Python is my mother tongue! Created by Guido van Rossum in 1991. ",
    ],

    # CodeAlpha
    ("codealpha", "internship", "intern"): [
        "CodeAlpha is a great software development company! This chatbot is an internship project. ",
        "CodeAlpha offers enriching internships with hands-on projects. You're part of it!",
    ],

    # Insults / frustration (gentle response)
    ("useless", "stupid", "dumb", "idiot", "terrible"): [
        "I'm still learning, please be patient with me! ",
        "I'm doing my best with predefined rules. Help me improve!",
        "I'm sorry to disappoint you… I promise to do better! ",
    ],
}

# Default response if nothing matches
DEFAULT_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that? ",
    "Hmm, I don't have a precise answer for that. Try different words!",
    "Good question! But my knowledge base is still limited. ",
    "I'm just a simple chatbot… Could you clarify your question?",
]


# ── Functions ────────────────────────────────────────────────

def normalize(text: str) -> str:
    """
    Normalize the input text:
    lowercase, remove punctuation.
    """
    text = text.lower().strip()
    # Remove punctuation except spaces
    text = re.sub(r"[^\w\s]", "", text)
    return text


def get_response(user_input: str) -> str:
    """
    Look for a response in the knowledge base.
    Returns a random response from the matching entry.
    """
    text = normalize(user_input)

    # Dynamic response for time/date
    time_words = {"time", "what time", "date", "today", "what day"}
    if any(word in text for word in time_words):
        now = datetime.now()
        return (
            f"It is currently {now.strftime('%I:%M %p')} "
            f"and today is {now.strftime('%B %d, %Y')}. "
        )

    # Search the knowledge base
    for triggers, responses in RESPONSES.items():
        for keyword in triggers:
            if keyword in text:
                valid_responses = [r for r in responses if r is not None]
                if valid_responses:
                    return random.choice(valid_responses)

    # No match found
    return random.choice(DEFAULT_RESPONSES)


def display_help():
    """Display the topics the bot can handle."""
    print("""
   Available topics:
  ─────────────────────────────────────────
  • Greetings      : hello, hi, hey…
  • Well-being     : how are you?
  • Identity       : who are you? your name?
  • Time / Date    : what time is it?
  • Joke           : tell me a joke
  • Python         : python, programming…
  • CodeAlpha      : internship, codealpha…
  • Goodbye        : bye, goodbye…
  ─────────────────────────────────────────
  Type 'quit' to exit.
    """)


def start_chatbot():
    """Launch the interactive chat session."""
    print("=" * 50)
    print("     CODEBOT — CodeAlpha Chatbot")
    print("=" * 50)
    print("  Hello! I'm CodeBot. I can answer your questions and chat with you.")
    print("  Type 'help' to see what I can do.")
    print("  Type 'quit' to end the session.")
    print("-" * 50)
    print()

    while True:
        # User input
        try:
            user_input = input("  You     : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  CodeBot : Goodbye! \n")
            break

        # Empty input
        if not user_input:
            print("  CodeBot : You didn't type anything. Ask me a question!\n")
            continue

        # Help command
        if normalize(user_input) == "help":
            display_help()
            continue

        # Quit command
        if normalize(user_input) in ("quit", "exit", "q"):
            print("  CodeBot : Goodbye! I hope I was helpful. \n")
            break

        # Get and display response
        response = get_response(user_input)
        print(f"  CodeBot : {response}\n")


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    start_chatbot()