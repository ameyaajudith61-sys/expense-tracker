"""
Simple Expense Tracker
-----------------------
A command-line app to add expenses, view them, and calculate total spending.
Data is stored in a local JSON file (expenses.json) so it persists between runs.
"""

import json
import os
from datetime import date

DATA_FILE = "expenses.json"


def load_expenses():
    """Load expenses from the JSON file, or return an empty list if none exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"Error: {DATA_FILE} contains invalid JSON. Fix or remove the file before continuing."
        ) from error


def save_expenses(expenses):
    """Save the expenses list to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    """Prompt the user for expense details and add it to the list."""
    description = input("Description: ").strip()
    while not description:
        description = input("Description cannot be empty. Try again: ").strip()

    while True:
        amount_input = input("Amount: ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    category = input("Category (e.g. Food, Transport, Fun) [Other]: ").strip()
    if not category:
        category = "Other"

    expense = {
        "description": description,
        "amount": round(amount, 2),
        "category": category,
        "date": str(date.today()),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added: {description} - ₵{amount:.2f}\n")


def view_expenses(expenses):
    """Print all expenses in a readable table."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print("\n%-4s %-12s %-20s %-12s %12s" % ("#", "Date", "Description", "Category", "Amount"))
    print("-" * 64)
    for i, e in enumerate(expenses, start=1):
        print("%-4d %-12s %-20s %-12s %12s" % (
            i, e["date"], e["description"][:20], e["category"][:12], f"₵{e['amount']:.2f}"
        ))
    print()


def calculate_total(expenses):
    """Print the total spending, and a breakdown by category."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal spending: ₵{total:.2f}")

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    print("\nBreakdown by category:")
    for category, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {category:<12} ₵{amount:.2f}")
    print()


def print_menu():
    print("=" * 30)
    print("      EXPENSE TRACKER")
    print("=" * 30)
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Calculate total spending")
    print("4. Exit")


def main():
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            calculate_total(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()