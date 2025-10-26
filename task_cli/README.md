# CLI Task Tracker

A simple, pure python implementation of a command line task tracker. 

## Features
- Adding tasks
- Updating task description
- Updating task status
- Deleting task
- Listing tasks by matching status

## Usage

First clone the repo and go the task_cli directory

```bash
git clone https://github.com/strunk23/python-projects.git
cd task_cli/
```

You can now use the CLI by typing the following commands. 

```bash
# Add task
python task_cli.py add Buy groceries
# Outputs: Task added successfully with ID: 1

# Update and delete
python task_cli.py update 1 "Buy groceries and cook dinner"
python task_cli.py delete 1

# Marking a task as in progress or done
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# Listing all tasks
python task_cli.py list

# Listing tasks by status
python task_cli.py list done
python task_cli.py list todo
python task_cli.py list in-progress
```


Project based on [roadmap.sh](https://roadmap.sh/projects/task-tracker)
