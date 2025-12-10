import os
import csv
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, Union


DATA_PATH: Path = Path(__file__).parent / "data.json"
BUDGET_PATH: Path = Path(__file__).parent / "budget.json"


def _load_json(path: Path) -> Dict[str, dict]:
    if not path.exists() or os.stat(path).st_size == 0:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_json(data: Dict[str, dict]) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def _create_budget() -> None:
    budget: Dict[str, str] = {}
    for month in range(1, 13):
        budget[str(month)] = 0.0

    with open(BUDGET_PATH, "w") as f:
        json.dump(budget, f, indent=4)

def add(description: str, amount: float, category: str) -> None:
    if amount <= 0:
        print("Provide a positive budget amount.")
        return
    
    month = str(datetime.date.today().month)
    budget = _load_json(BUDGET_PATH)

    if summary(month, False) > budget.get(month):
        print("Warning! You have exceeded the budget for this month.")

    data = _load_json(DATA_PATH)
    next_id = str(max(map(int, data.keys()), default=0) + 1)
    new_expense = {
        "description": description,
        "date": str(datetime.date.today()),
        "amount": amount,
        "category": category if category is not None else "No category"
    }
    data[next_id] = new_expense
    _save_json(data)
    print(f"Expense added successfully with ID: {next_id}")

def update(expense_id: str, new_description: Union[str, None], new_amount: Union[float, None], new_category: Union[str, None]) -> None:
    data = _load_json(DATA_PATH)
    expense = data.get(expense_id)

    if not expense:
        print(f"No expense with id {expense_id} found.")
        return
    
    if new_amount: expense["amount"] = new_amount
    if new_category: expense["category"] = new_category
    if new_description: expense["description"] = new_description

    data[expense_id] = expense
    _save_json(data)

def list_expenses(category: Union[str, None]) -> None:
    data = _load_json(DATA_PATH)

    for key, value in data.items():
        if value.get("category") != category and category:
            continue
        
        print({'id': int(key), **value})

def summary(month: Union[str, None], out: bool = True) -> int:
    expense_sum = 0

    data = _load_json(DATA_PATH)
    for expense in data.values():
        print(data)
        if month is None:
            expense_sum += expense.get("amount")
        elif str(datetime.datetime.strptime(expense.get("date"), "%Y-%m-%d").month) == month:
            expense_sum += expense.get("amount")

    if out:
        print(f"Total expenses: {expense_sum}")
    return expense_sum

def delete(expense_id: str) -> None:
    data = _load_json(DATA_PATH)
    if expense_id not in data:
        print(f"No expense with id {expense_id} found.")
        return
    data.pop(expense_id)
    _save_json(data)

def budget(month: str, amount: float) -> None:
    if not BUDGET_PATH.exists() or os.stat(BUDGET_PATH).st_size == 0:
        _create_budget()

    if amount <= 0:
        print("Provide a positive budget amount.")
        return

    data = _load_json(BUDGET_PATH)
    data[month] = amount
    with open(BUDGET_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def export(path: str) -> None:
    if not os.path.exists(path):
        print("Please provide a valid path.")
        return

    data = _load_json(DATA_PATH)
    rows = []
    for key, value in data.items():
        row = {"id": key, **value}
        rows.append(row)

    with open(Path(path) / "export.csv", "w", newline="", encoding="UTF-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="A simple command-line expense tracking tool.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new expense.")
    add_parser.add_argument("--description", "-d", type=str, required=True, help="Description of the expense.")
    add_parser.add_argument("--amount", "-a", type=float, required=True, help="Amount of the expense.")
    add_parser.add_argument("--category", "-c", type=str, required=False, help="Category of the expense.")

    update_parser = subparsers.add_parser("update", help="Update a selected expense.")
    update_parser.add_argument("--id", "-i", type=str, required=True, help="ID of the expense to update.")
    update_parser.add_argument("--description", "-d", type=str, required=False, help="Description of the expense.")
    update_parser.add_argument("--amount", "-a", type=float, required=False, help="Amount of the expense.")
    update_parser.add_argument("--category", "-c", type=str, required=False, help="Category of the expense.")

    list_parser = subparsers.add_parser("list", help="List all expenses.")
    list_parser.add_argument("--category", "-c", type=str, required=False, help="Expense category to filter by.")

    summary_parser = subparsers.add_parser("summary", help="Show expense summary.")
    summary_parser.add_argument("--month", "-m", type=str, required=False, help="Filter summary by month (1–12).")

    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID.")
    delete_parser.add_argument("--id", "-i", type=str, required=True, help="ID of the expense to delete.")

    budget_parser = subparsers.add_parser("budget", help="Add a budget.")
    budget_parser.add_argument("--month", "-m", type=str, required=True, help="Month to set a budget for.")
    budget_parser.add_argument("--amount", "-a", type=float, required=True, help="Budget amount.")

    export_parser = subparsers.add_parser("export", help="Export all expenses to a CSV file")
    export_parser.add_argument("--path", "-p", type=str, required=True, help="Path where the file will be created.")

    args = parser.parse_args()

    if args.command == "add":
        add(args.description, args.amount, args.category)
    elif args.command == "update":
        update(args.id, args.description, args.amount, args.category)
    elif args.command == "list":
        list_expenses(args.category)
    elif args.command == "summary":
        summary(args.month)
    elif args.command == "delete":
        delete(args.id)
    elif args.command == "budget":
        budget(args.month, args.amount)
    elif args.command == "export":
        export(args.path)

if __name__ == "__main__":
    main()
