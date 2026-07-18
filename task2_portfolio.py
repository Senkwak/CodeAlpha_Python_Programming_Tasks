# ============================================================
#  TASK 2 — STOCK PORTFOLIO TRACKER
#  CodeAlpha Python Internship
#  Concepts: dictionary, I/O, arithmetic, file handling
# ============================================================

import csv
import os
from datetime import datetime

# ── Hardcoded stock prices (USD) ─────────────────────────────
STOCK_PRICES = {
    "AAPL":  182.50,   # Apple
    "TSLA":  248.00,   # Tesla
    "GOOGL": 175.30,   # Alphabet (Google)
    "MSFT":  415.20,   # Microsoft
    "AMZN":  189.90,   # Amazon
    "META":  502.10,   # Meta (Facebook)
    "NVDA":  875.40,   # NVIDIA
    "NFLX":  635.00,   # Netflix
}

CSV_FILE = "portfolio.csv"
TXT_FILE = "portfolio.txt"


# ── Utility functions ────────────────────────────────────────

def display_available_stocks():
    """Display the list of available stocks with their prices."""
    print("\n  Available stocks:")
    print("  " + "─" * 38)
    print(f"  {'Symbol':<10} {'Name':<20} {'Price (USD)':>8}")
    print("  " + "─" * 38)
    names = {
        "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Alphabet",
        "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta",
        "NVDA": "NVIDIA", "NFLX": "Netflix",
    }
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<10} {names[symbol]:<20} {price:>8.2f} $")
    print("  " + "─" * 38)


def input_portfolio():
    """
    Ask the user to enter their stocks and quantities.
    Returns a dictionary {symbol: quantity}.
    """
    portfolio = {}
    print("\n Enter your stocks (type 'done' to finish)\n")

    while True:
        symbol = input("  Stock symbol: ").strip().upper()

        if symbol == "DONE":
            break

        if symbol not in STOCK_PRICES:
            print(f"  '{symbol}' is not available. Choose from the list.\n")
            continue

        # Quantity input
        while True:
            try:
                qty = int(input(f"  Quantity of {symbol}: ").strip())
                if qty <= 0:
                    print("  Quantity must be a positive integer.")
                    continue
                break
            except ValueError:
                print("  Please enter a valid integer.")

        # Add or accumulate
        if symbol in portfolio:
            portfolio[symbol] += qty
            print(f" Updated: {symbol} → {portfolio[symbol]} shares\n")
        else:
            portfolio[symbol] = qty
            print(f" Added: {symbol} × {qty}\n")

    return portfolio


def calculate_values(portfolio):
    """
    Calculate the value per line and the total.
    Returns a list of tuples (symbol, quantity, price, value).
    """
    lines = []
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        lines.append((symbol, qty, price, value))
    return lines


def display_report(lines):
    """Display the portfolio report in the console."""
    total = sum(v for _, _, _, v in lines)
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")

    print()
    print("  " + "═" * 56)
    print("   STOCK PORTFOLIO REPORT")
    print(f"             {timestamp}")
    print("  " + "═" * 56)
    print(f"  {'Symbol':<10} {'Qty':>6}  {'Unit price':>12}  {'Value':>13}")
    print("  " + "─" * 56)

    for symbol, qty, price, value in lines:
        print(f"  {symbol:<10} {qty:>6}  {price:>10.2f} $  {value:>11.2f} $")

    print("  " + "─" * 56)
    print(f"  {'TOTAL':>36}  {total:>11.2f} $")
    print("  " + "═" * 56)
    print(f"\n  Total portfolio value: {total:,.2f} USD\n")

    return total, timestamp


def save_csv(lines, total, timestamp):
    """Save the portfolio to a CSV file."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Symbol", "Quantity", "Unit Price (USD)", "Value (USD)"])
        for symbol, qty, price, value in lines:
            writer.writerow([timestamp, symbol, qty, f"{price:.2f}", f"{value:.2f}"])
        writer.writerow([])
        writer.writerow(["", "", "", "TOTAL", f"{total:.2f}"])
    print(f" Saved as CSV → {os.path.abspath(CSV_FILE)}")


def save_txt(lines, total, timestamp):
    """Save the portfolio to a readable text file."""
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 56 + "\n")
        f.write("   STOCK PORTFOLIO REPORT\n")
        f.write(f"   Date: {timestamp}\n")
        f.write("=" * 56 + "\n")
        f.write(f"{'Symbol':<10} {'Qty':>6}  {'Unit price':>12}  {'Value':>13}\n")
        f.write("-" * 56 + "\n")
        for symbol, qty, price, value in lines:
            f.write(f"{symbol:<10} {qty:>6}  {price:>10.2f} $  {value:>11.2f} $\n")
        f.write("-" * 56 + "\n")
        f.write(f"{'TOTAL':>36}  {total:>11.2f} $\n")
        f.write("=" * 56 + "\n")
    print(f" Saved as TXT → {os.path.abspath(TXT_FILE)}")


def main():
    print("=" * 56)
    print("    STOCK PORTFOLIO TRACKER — CodeAlpha")
    print("=" * 56)

    # Display available stocks
    display_available_stocks()

    # Input portfolio
    portfolio = input_portfolio()

    if not portfolio:
        print("\n   No stocks entered. Exiting.\n")
        return

    # Calculate and display
    lines = calculate_values(portfolio)
    total, timestamp = display_report(lines)

    # Optional save
    choice = input("   Save the result? (csv / txt / both / no): ").strip().lower()
    print()
    if choice in ("csv", "both"):
        save_csv(lines, total, timestamp)
    if choice in ("txt", "both"):
        save_txt(lines, total, timestamp)
    if choice == "no":
        print("   Result not saved.")

    print("\n  Done. Happy investing!\n")


if __name__ == "__main__":
    main()