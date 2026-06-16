import argparse
from src.storage_manager import StorageManager
from rich.console import Console
from rich.table import Table

console = Console()

def handle_add_user(args, storage):
    users = storage.load_data()
    if args.name in users:
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' already exists.")
        return
    users[args.name] = User(args.name)
    storage.save_data(users)
    console.print(f"[bold green]Success:[/bold green] User '{args.name}' created.")

def handle_add_project(args, storage):
    users = storage.load_data()
    if args.user not in users:
        console.print(f"[bold red]Error:[/bold red] User '{args.user}' not found. Create them first.")
        return
    
    user = users[args.user]
    # Check if project name already exists for this user
    if any(p.title.lower() == args.title.lower() for p in user.projects):
        console.print(f"[bold yellow]Warning:[/bold yellow] Project '{args.title}' already exists for {args.user}.")
        return

    project = user.add_project(args.title)
    storage.save_data(users)
    console.print(f"[bold green]Success:[/bold green] Project '{project.title}' (ID: {project.id}) added to {args.user}.")

def handle_add_task(args, storage):
    users = storage.load_data()
    project_found = False
    
    for user in users.values():
        for project in user.projects:
            if project.title.lower() == args.project.lower() or project.id == args.project:
                task = project.add_task(args.title)
                project_found = True
                break
        if project_found:
            break

    if project_found:
        storage.save_data(users)
        console.print(f"[bold green]Success:[/bold green] Task '{args.title}' (ID: {task.id}) added to project '{args.project}'.")
    else:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found anywhere in system.")

def handle_list_all(args, storage):
    users = storage.load_data()
    if not users:
        console.print("[yellow]The system is currently empty.[/yellow]")
        return

    table = Table(title="Project Management Dashboard", show_lines=True)
    table.add_column("User", style="cyan", no_wrap=True)
    table.add_column("Projects [ID]", style="magenta")
    table.add_column("Tasks [ID] (Status)", style="green")

    for user_name, user_obj in users.items():
        if not user_obj.projects:
            table.add_row(user_name, "[italic dim]No Projects[/italic dim]", "-")
            continue
        
        for project in user_obj.projects:
            task_strs = []
            for t in project.tasks:
                status = "✅ Done" if t.is_completed else "⏳ Pending"
                task_strs.append(f"• {t.title} [{t.id}] ({status})")
            
            tasks_output = "\n".join(task_strs) if task_strs else "[italic dim]No Tasks[/italic dim]"
            table.add_row(user_name, f"{project.title} [{project.id}]", tasks_output)
            
    console.print(table)

def handle_complete_task(args, storage):
    users = storage.load_data()
    task_updated = False
    
    for user in users.values():
        for project in user.projects:
            for task in project.tasks:
                if task.id == args.task_id:
                    task.mark_complete()
                    task_updated = True
                    break
            if task_updated: break
        if task_updated: break

    if task_updated:
        storage.save_data(users)
        console.print(f"[bold green]Success:[/bold green] Task [{args.task_id}] marked complete!")
    else:
        console.print(f"[bold red]Error:[/bold red] Task ID [{args.task_id}] could not be found.")

def build_cli():
    parser = argparse.ArgumentParser(description="Multi-User Project Management Command-Line Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # User Subcommand
    u_parser = subparsers.add_parser("add-user", help="Register a new system user")
    u_parser.add_argument("--name", required=True, help="Unique name of the user")
    u_parser.set_defaults(func=handle_add_user)

    # Project Subcommand
    p_parser = subparsers.add_parser("add-project", help="Assign a new project to an existing user")
    p_parser.add_argument("--user", required=True, help="Name of the user owner")
    p_parser.add_argument("--title", required=True, help="Title of the project")
    p_parser.set_defaults(func=handle_add_project)

    # Task Subcommand
    t_parser = subparsers.add_parser("add-task", help="Append a task to an existing project")
    t_parser.add_argument("--project", required=True, help="Project title or Project ID")
    t_parser.add_argument("--title", required=True, help="Task description summary")
    t_parser.set_defaults(func=handle_add_task)

    # Complete Task Subcommand
    c_parser = subparsers.add_parser("complete-task", help="Mark a specific task completed via its unique ID")
    c_parser.add_argument("--task-id", required=True, help="8-character unique Task alphanumeric hash")
    c_parser.set_defaults(func=handle_complete_task)

    # List Subcommand
    l_parser = subparsers.add_parser("list", help="Render interactive system dashboard data matrix")
    l_parser.set_defaults(func=handle_list_all)

    return parser