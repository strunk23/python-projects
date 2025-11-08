# CLI Task Tracker

A simple, pure python implementation of a command line expense tracker. 

## Features
- Adding expenses
- Updating expenses
- Deleting expenses
- Listing expenses
- Exporting expenses to a CSV file
- Budget setting for each month
- Summary of all expenses

## Usage

First clone the repo and go the expense_tracker directory

```bash
git clone https://github.com/strunk23/python-projects.git
cd python-projects/expense_tracker/
```

You can now use the tracker by typing the following commands. 

```bash
# Add expense
python expense_tracker.py add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)

python expense_tracker.py add --description "Dinner" --amount 10 --category "School"
# Expense added successfully (ID: 2)

# List expenses
python expense_tracker.py list
# {'id': 1, 'description': 'Lunch', 'date': '2025-11-02', 'amount': 20.0, 'category': 'No category'}
# {'id': 2, 'description': 'Dinner', 'date': '2025-11-02', 'amount': 10.0, 'category': 'School'}

# Summary of all expenses
python expense_tracker.py summary
# Total expenses: 30.0

# Delete a specific expense
python expense_tracker.py delete --id 2

# Summary for a given month
python expense_tracker.py summary --month 8
# Total expenses: $20

# Budget for a given month
python expense_tracker.py budget --month 10 --amount 100

# Export to a CSV file
python expense_tracker.py export --path /home/user/
```

Project based on [roadmap.sh](https://roadmap.sh/projects/expense-tracker)