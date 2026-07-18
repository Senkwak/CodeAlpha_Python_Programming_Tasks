# ============================================================
#  TASK 1 — HANGMAN GAME
#  CodeAlpha Python Internship
#  Concepts: random, while, if-else, strings, lists
# ============================================================

import random

# ── Predefined word list ─────────────────────────────────────
WORDS = ["python", "keyboard", "window", "language", "loop"]

# ── Hangman drawings (7 stages: 0 wrong → 6 wrong) ──────────
HANGMAN = [
    """
       ┌──────┐
       │      │
              │
              │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
              │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
       │      │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│      │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
      /       │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
      / \\     │
              │
    ══════════╧══
    """,
]

MAX_WRONG = 6


def display_word(secret_word, found_letters):
    """Display the word with guessed letters and '_' for the rest."""
    display = ""
    for letter in secret_word:
        if letter in found_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()


def word_guessed(secret_word, found_letters):
    """Return True if all letters of the word have been found."""
    return all(letter in found_letters for letter in secret_word)


def play():
    """Main function of the Hangman game."""
    print("=" * 45)
    print("      🎮  WELCOME TO THE HANGMAN GAME  🎮")
    print("=" * 45)

    # Pick a random word
    secret_word = random.choice(WORDS)
    found_letters = []    # correctly guessed letters
    wrong_letters = []    # incorrect guesses
    nb_wrong = 0

    print(f"\nI picked a word with {len(secret_word)} letters. Good luck!\n")

    # ── Main game loop ───────────────────────────────────────
    while nb_wrong < MAX_WRONG:
        # Show hangman drawing
        print(HANGMAN[nb_wrong])

        # Show word state
        print(f"  Word   : {display_word(secret_word, found_letters)}")
        print(f"  Errors : {nb_wrong}/{MAX_WRONG}")
        print(f"  Wrong letters : {' '.join(wrong_letters) if wrong_letters else '—'}")
        print()

        # Ask for a letter
        guess = input("  👉 Enter a letter: ").strip().lower()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("  ⚠️  Please enter a single letter.\n")
            continue

        if guess in found_letters or guess in wrong_letters:
            print("  ⚠️  You already tried that letter.\n")
            continue

        # Check if the letter is in the word
        if guess in secret_word:
            found_letters.append(guess)
            print(f"  ✅ Nice! '{guess}' is in the word.\n")

            # Check if the full word has been guessed
            if word_guessed(secret_word, found_letters):
                print(HANGMAN[nb_wrong])
                print(f"  🎉 CONGRATULATIONS! You found the word: « {secret_word.upper()} »")
                print("=" * 45)
                break
        else:
            wrong_letters.append(guess)
            nb_wrong += 1
            print(f"  ❌ '{guess}' is not in the word. ({nb_wrong}/{MAX_WRONG})\n")

    else:
        # The player ran out of attempts
        print(HANGMAN[MAX_WRONG])
        print(f"  💀 GAME OVER! The word was: « {secret_word.upper()} »")
        print("=" * 45)


def main():
    """Loop allowing the player to replay."""
    while True:
        play()
        again = input("\n🔄 Do you want to play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n👋 Thanks for playing. See you next time!\n")
            break
        print()


if __name__ == "__main__":
    main()
