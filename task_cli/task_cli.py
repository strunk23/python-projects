import argparse
import json
import os
import datetime
from pathlib import Path
from typing import Dict, Optional

STATUS_TYPES = ["todo", "in-progress", "done"]

class TaskManager():
    JSON_PATH = Path(__file__).parent / "data.json" 

    def _timestamp(self) -> str:
        return f"{datetime.date.today()} / {datetime.datetime.now().strftime('%H-%M-%S')}"

    def _load_tasks(self) -> Dict[str, dict]:
        """Load all tasks from JSON or return empty dict if file doesn’t exist."""
        if not self.JSON_PATH.exists() or os.stat(self.JSON_PATH).st_size == 0:
            return {}
        with open(self.JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_tasks(self, data: Dict[str, dict]) -> None:
        """Write tasks to the JSON file."""
        with open(self.JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_task(self, description: str) -> None:
        data = self._load_tasks()
        next_id = str(max(map(int, data.keys()), default=0) + 1)
        new_task = {
            "description": description,
            "status": "todo",
            "createdAt": self._timestamp(),
            "updatedAt": self._timestamp()
        }
        data[next_id] = new_task
        self._save_tasks(data)
        print(f"Task added successfully with ID: {next_id}")

    def update_task(self, task_id: str, new_description: str) -> None:
        data = self._load_tasks()
        task = data.get(task_id)
        if not task:
            print(f"No task with id {task_id} found.")
            return
        task["description"] = new_description
        task["updatedAt"] = self._timestamp()
        data[task_id] = task
        self._save_tasks(data)

    def change_status(self, task_id: str, status: str) -> None:
        if status not in STATUS_TYPES:
            print(f"Invalid status '{status}'. Must be one of {STATUS_TYPES}")
            return
        data = self._load_tasks()
        task = data.get(task_id)
        if not task:
            print(f"No task with id {task_id} found.")
            return
        task["status"] = status
        task["updatedAt"] = self._timestamp()
        data[task_id] = task
        self._save_tasks(data)

    def delete_task(self, task_id: str) -> None:
        data = self._load_tasks()
        if task_id not in data:
            print(f"No task with id {task_id} found.")
            return
        data.pop(task_id)
        self._save_tasks(data)

    def list_tasks(self, status: Optional[str] = None) -> None:
        data = self._load_tasks()
        if not data:
            print("No tasks exist.")
            return
        matched = False
        for task_id, details in data.items():
            if status is None or details["status"] == status:
                matched = True
                print(
                    f"ID: {task_id}\n"
                    f"Description: {details['description']}\n"
                    f"Status: {details['status']}\n"
                    f"Created at: {details['createdAt']}\n"
                    f"Updated at: {details['updatedAt']}"
                )
        if not matched:
            print(f"No tasks with '{status}' status found.")

def main():
    parser = argparse.ArgumentParser(description="Simple Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Description of the task")

    update_parser = subparsers.add_parser("update", help="Update a task description")
    update_parser.add_argument("task_id", help="ID of the task")
    update_parser.add_argument("new_description", help="New description")

    mip_parser = subparsers.add_parser("mark-in-progress", help="Mark task as in progress")
    mip_parser.add_argument("task_id", help="ID of the task")

    md_parser = subparsers.add_parser("mark-done", help="Mark task as done")
    md_parser.add_argument("task_id", help="ID of the task")

    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("task_id", help="ID of the task")

    list_parser = subparsers.add_parser("list", help="List tasks (optionally filtered by status)")
    list_parser.add_argument("status_type", nargs="?", help="Status to filter by (optional)")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(args.description)
    elif args.command == "update":
        manager.update_task(args.task_id, args.new_description)
    elif args.command == "mark-in-progress":
        manager.change_status(args.task_id, "in-progress")
    elif args.command == "mark-done":
        manager.change_status(args.task_id, "done")
    elif args.command == "delete":
        manager.delete_task(args.task_id)
    elif args.command == "list":
        if args.status_type and args.status_type not in STATUS_TYPES:
            print(f"Invalid status type. Valid types: {STATUS_TYPES}")
        else:
            manager.list_tasks(args.status_type)

if __name__ == "__main__":
    main()
