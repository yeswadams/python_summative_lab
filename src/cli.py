import argparse
import sys
import logging
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from dateutil.parser import parse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.storage import Storage
from src.models import User, Project, Task

console = Console()
logger = logging.getLogger("PM-CLI.cli")

def format_date(iso_date: str) -> str:
    """Formats an ISO date string into a human-readable format."""
    try:
        dt = parse(iso_date)
        return dt.strftime("%b %d, %Y")
    except Exception:
        return iso_date

class UserInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class ProjectInput(BaseModel):
    user: str
    title: str = Field(..., min_length=2, max_length=100)

class TaskInput(BaseModel):
    project: str
    title: str = Field(..., min_length=2, max_length=200)

def handle_add_user(args, storage: Storage):
    try:
        data = UserInput(name=args.name)
        users = storage.load_data()
        if data.name in users:
            console.print(Panel(f"[bold red]Error:[/bold red] User '{data.name}' already exists.", border_style="red"))
            return
        
        users[data.name] = User(name=data.name)
        storage.save_data(users)
        console.print(Panel(f"[bold green]Success:[/bold green] User '{data.name}' created successfully.", border_style="green"))
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red] {e.errors()[0]['msg']}", border_style="red"))

def handle_add_project(args, storage: Storage):
    try:
        data = ProjectInput(user=args.user, title=args.title)
        users = storage.load_data()
        if data.user not in users:
            console.print(Panel(f"[bold red]Error:[/bold red] User '{data.user}' not found.", border_style="red"))
            return
        
        user = users[data.user]
        user.add_project(data.title)
        storage.save_data(users)
        console.print(Panel(f"[bold green]Success:[/bold green] Project '{data.title}' added to user '{data.user}'.", border_style="green"))
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red] {e.errors()[0]['msg']}", border_style="red"))

def handle_add_task(args, storage: Storage):
    try:
        data = TaskInput(project=args.project, title=args.title)
        users = storage.load_data()
        found = False
        for user in users.values():
            for project in user.projects:
                if project.title == data.project or project.id == data.project:
                    project.add_task(data.title)
                    found = True
                    break
            if found: break
        
        if found:
            storage.save_data(users)
            console.print(Panel(f"[bold green]Success:[/bold green] Task added to project '{data.project}'.", border_style="green"))
        else:
            console.print(Panel(f"[bold red]Error:[/bold red] Project '{data.project}' not found.", border_style="red"))
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red] {e.errors()[0]['msg']}", border_style="red"))

def handle_complete_task(args, storage: Storage):
    users = storage.load_data()
    found = False
    for user in users.values():
        for project in user.projects:
            for task in project.tasks:
                if task.id == args.task_id:
                    task.mark_complete()
                    found = True
                    break
            if found: break
        if found: break
    
    if found:
        storage.save_data(users)
        console.print(Panel(f"[bold green]Success:[/bold green] Task '{args.task_id}' marked as complete.", border_style="green"))
    else:
        console.print(Panel(f"[bold red]Error:[/bold red] Task ID '{args.task_id}' not found.", border_style="red"))

def handle_list(args, storage: Storage):
    users = storage.load_data()
    if not users:
        console.print("[yellow]No data found in the system.[/yellow]")
        return

    table = Table(title="Project Tracker Dashboard", show_lines=True, header_style="bold magenta")
    table.add_column("User", style="cyan")
    table.add_column("Projects", style="green")
    table.add_column("Tasks (Status)", style="white")

    for user in users.values():
        if not user.projects:
            table.add_row(user.name, "[dim]No projects[/dim]", "-")
            continue
        
        for project in user.projects:
            project_created = format_date(project.created_at)
            task_info = []
            for task in project.tasks:
                status = "[green]✔[/green]" if task.is_completed else "[yellow]⏳[/yellow]"
                task_info.append(f"{status} {task.title} ([dim]{task.id}[/dim])")
            
            tasks_display = "\n".join(task_info) if task_info else "[dim]No tasks[/dim]"
            table.add_row(
                user.name, 
                f"{project.title}\n([dim]{project.id}[/dim])\n[italic dim]Created: {project_created}[/italic dim]", 
                tasks_display
            )

    console.print(table)

def build_cli():
    parser = argparse.ArgumentParser(description="Advanced Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add-user
    user_parser = subparsers.add_parser("add-user", help="Add a new user")
    user_parser.add_argument("--name", required=True, help="User name")
    user_parser.set_defaults(func=handle_add_user)

    # add-project
    project_parser = subparsers.add_parser("add-project", help="Add a new project")
    project_parser.add_argument("--user", required=True, help="User name")
    project_parser.add_argument("--title", required=True, help="Project title")
    project_parser.set_defaults(func=handle_add_project)

    # add-task
    task_parser = subparsers.add_parser("add-task", help="Add a new task")
    task_parser.add_argument("--project", required=True, help="Project ID or title")
    task_parser.add_argument("--title", required=True, help="Task title")
    task_parser.set_defaults(func=handle_add_task)

    # complete-task
    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("--task-id", required=True, help="Task ID")
    complete_parser.set_defaults(func=handle_complete_task)

    # list
    list_parser = subparsers.add_parser("list", help="List all users, projects, and tasks")
    list_parser.set_defaults(func=handle_list)

    return parser

def main_execution():
    parser = build_cli()
    args = parser.parse_args()
    storage = Storage()

    try:
        args.func(args, storage)
    except Exception as e:
        logger.exception("A global error occurred during execution.")
        console.print(Panel(f"[bold red]Unexpected Error:[/bold red] {str(e)}", border_style="red"))
        sys.exit(1)
