# CodeAlpha — Python Programming Internship 

Repository containing my completed tasks for the **CodeAlpha Python Programming Internship**.

CodeAlpha is a software development company offering hands-on internship programs in Python development and scripting, covering fundamentals, data structures, file handling, OOP concepts, and popular libraries such as Pandas, NumPy, and Flask.

This repository includes **4 completed tasks**.
---

## Repository Structure

```
CodeAlpha_Python_Programming_Tasks/
├── python/
│   ├── task1_hangman.py
│   ├── task2_portfolio.py
│   ├── task3_automation.py
│   └── task4_chatbot.py
|
└── README.md
```

---

## Task 1 — Hangman Game
A text-based Hangman game where the player guesses a word one letter at a time.
- 5 predefined words, chosen randomly
- Maximum of 6 incorrect guesses
- ASCII-art hangman drawing that updates with each mistake
- Console input/output only

**Concepts used:** `random`, `while` loop, `if-else`, strings, lists

---

## Task 2 — Stock Portfolio Tracker
A simple stock tracker that calculates total investment value based on hardcoded stock prices.
- User inputs stock symbols and quantities
- Hardcoded dictionary of stock prices (e.g. `{"AAPL": 182.50, "TSLA": 248.00}`)
- Displays a formatted investment report with total value
- Optional export to `.csv` or `.txt`

**Concepts used:** dictionary, input/output, arithmetic, file handling (optional)

---

## Task 3 — Task Automation with Python Scripts
A menu-driven automation tool offering 3 real-life automation options:
- **A.** Move all `.jpg` files from a folder to a new folder
- **B.** Extract all email addresses from a `.txt` file using regex and save them
- **C.** Scrape the `<title>` of a fixed webpage and save it

**Concepts used:** `os`, `shutil`, `re`, `requests`, file handling

---

## Task 4 — Basic Chatbot
A rule-based chatbot that responds to common user inputs.
- Recognizes greetings, small talk, jokes, and more
- Dynamic responses (e.g. current time/date)
- Randomized replies to keep the conversation natural

**Concepts used:** `if-elif`, functions, loops, input/output

---

## How to Run

Each script is standalone and requires **Python 3**. Some tasks in `task3` require the `requests` library:

```bash
pip install requests
```

Run any script directly:

```bash
python task1_hangman.py
```

---

## About CodeAlpha

Website: [www.codealpha.tech](https://www.codealpha.tech)

Internship perks: Internship Offer Letter, Completion Certificate (QR Verified), Unique ID Certificate, Letter of Recommendation, Job Opportunities, and Resume Building Support.

---

## License

This project is for educational purposes as part of the CodeAlpha internship program.
