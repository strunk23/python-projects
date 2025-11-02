import os
import csv
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, Union, Any


class Tracker():
    _DATA_PATH: Path = Path(__file__).parent / "data.json"
    _BUDGET_PATH : Path = Path(__file__).parent / "budget.json"

    def __init__(self):
        if not os.path.exists(self._BUDGET_PATH):
            self._create_budget()

    def _load_json(self, path: Path) -> Dict[str, dict]:
        if not path.exists() or os.stat(path).st_size == 0:
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, data: Dict[str, dict]) -> None:
        with open(self._DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _create_budget(self) -> None:
        budget: Dict[str, str] = {}
        for month in range(1, 13):
            budget[str(month)] = 0.0

        with open(self._BUDGET_PATH, "w") as f:
            json.dump(budget, f, indent=4)

    def add(self, description: str, amount: float, category: str) -> None:
        if amount <= 0:
            print("Provide a positive budget amount.")
            return
        
        month = str(datetime.date.today().month)
        budget = self._load_json(self._BUDGET_PATH)

        if self.summary(month, False) > budget.get(month):
            print("Warning! You have exceeded the budget for this month.")

        data = self._load_json(self._DATA_PATH)
        next_id = str(max(map(int, data.keys()), default=0) + 1)
        new_expense = {
            "description": description,
            "date": str(datetime.date.today()),
            "amount": amount,
            "category": category if category is not None else "No category"
        }
        data[next_id] = new_expense
        self._save_json(data)
        print(f"Expense added successfully with ID: {next_id}")

    def update(self, expense_id: str, new_description: Union[str, None], new_amount: Union[float, None], new_category: Union[str, None]) -> None:
        data = self._load_json(self._DATA_PATH)
        expense = data.get(expense_id)

        if not expense:
            print(f"No expense with id {expense_id} found.")
            return
        
        if new_amount: expense["amount"] = new_amount
        if new_category: expense["category"] = new_category
        if new_description: expense["description"] = new_description

        data[expense_id] = expense
        self._save_json(data)

    def list_expenses(self, category: Union[str, None]) -> None:
        data = self._load_json(self._DATA_PATH)

        for key, value in data.items():
            if value.get("category") != category and category:
                continue
            
            print({'id': int(key), **value})

    def summary(self, month: Union[str, None], out: bool = True) -> int:
        expense_sum = 0

        data = self._load_json(self._DATA_PATH)
        for expense in data.values():
            if month is None:
                expense_sum += expense.get("amount")
            elif str(datetime.datetime.strptime(expense.get("date"), "%Y-%m-%d").month) == month:
                expense_sum += expense.get("amount")

        if out:
            print(f"Total expenses: {expense_sum}")
        return expense_sum

    def delete(self, expense_id: str) -> None:
        data = self._load_json(self._DATA_PATH)
        if expense_id not in data:
            print(f"No expense with id {expense_id} found.")
            return
        data.pop(expense_id)
        self._save_json(data)

    def budget(self, month: str, amount: float) -> None:
        if amount <= 0:
            print("Provide a positive budget amount.")
            return

        data = self._load_json(self._BUDGET_PATH)
        data[month] = amount
        with open(self._BUDGET_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def export(self, path: str) -> None:
        if not os.path.exists(path):
            print("Please provide a valid path.")
            return

        data = self._load_json(self._DATA_PATH)
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
    tracker = Tracker()

    if args.command == "add":
        tracker.add(args.description, args.amount, args.category)
    elif args.command == "update":
        tracker.update(args.id, args.description, args.amount, args.category)
    elif args.command == "list":
        tracker.list_expenses(args.category)
    elif args.command == "summary":
        tracker.summary(args.month)
    elif args.command == "delete":
        tracker.delete(args.id)
    elif args.command == "budget":
        tracker.budget(args.month, args.amount)
    elif args.command == "export":
        tracker.export(args.path)

if __name__ == "__main__":
    main()
