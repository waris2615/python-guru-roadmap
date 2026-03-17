"""CLI interface for Logic Engine."""
import argparse
import sys
from task import TaskDatabase, Task


def list_tasks(db: TaskDatabase):
    tasks = db.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        print(f"[{t.id}] {t.title} - {t.status}")
        if t.description:
            print(f"    {t.description}")


def add_task(db: TaskDatabase, title: str, description: str = ""):
    task = db.add_task(title, description)
    print(f"Created task #{task.id}: {task.title}")


def complete_task(db: TaskDatabase, task_id: int):
    if db.update_status(task_id, 'completed'):
        print(f"Task {task_id} marked completed.")
    else:
        print(f"Task {task_id} not found.")


def delete_task(db: TaskDatabase, task_id: int):
    if db.delete_task(task_id):
        print(f"Task {task_id} deleted.")
    else:
        print(f"Task {task_id} not found.")


def main():
    parser = argparse.ArgumentParser(description="Logic Engine CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    
    sub.add_parser("list", help="List all tasks")
    sub.add_parser("ls", help="List all tasks (short)")
    
    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")
    add_p.add_argument("-d", "--description", default="", help="Task description")
    
    done_p = sub.add_parser("done", help="Mark task as completed")
    done_p.add_argument("id", type=int, help="Task ID")
    
    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int, help="Task ID")
    
    args = parser.parse_args()
    
    with TaskDatabase("tasks.db") as db:
        if args.command in ("list", "ls"):
            list_tasks(db)
        elif args.command == "add":
            add_task(db, args.title, args.description)
        elif args.command == "done":
            complete_task(db, args.id)
        elif args.command == "delete":
            delete_task(db, args.id)


if __name__ == "__main__":
    main()