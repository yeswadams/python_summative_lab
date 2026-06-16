import uuid
from typing import List, Dict, Any

class Task:
    def __init__(self, title: str, task_id: str = "", is_completed: bool = False):
        self.id = task_id if task_id else str(uuid.uuid4())[:8]
        self.title = title
        self.is_completed = is_completed

    def mark_complete(self):
        self.is_completed = True

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "title": self.title, "is_completed": self.is_completed}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(title=data["title"], task_id=data["id"], is_completed=data["is_completed"])


class Project:
    def __init__(self, title: str, project_id: str = ""):
        self.id = project_id if project_id else str(uuid.uuid4())[:8]
        self.title = title
        self.tasks: List[Task] = []

    def add_task(self, task_title: str) -> Task:
        new_task = Task(task_title)
        self.tasks.append(new_task)
        return new_task

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        project = cls(title=data["title"], project_id=data["id"])
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project


class User:
    def __init__(self, name: str):
        self.name = name
        self.projects: List[Project] = []

    def add_project(self, project_title: str) -> Project:
        new_project = Project(project_title)
        self.projects.append(new_project)
        return new_project

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "projects": [project.to_dict() for project in self.projects]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        user = cls(name=data["name"])
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return user