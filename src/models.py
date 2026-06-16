import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional

class Entity(ABC):
    """Abstract base class for all domain entities."""
    def __init__(self, entity_id: Optional[str] = None, created_at: Optional[str] = None):
        self._id = entity_id or str(uuid.uuid4())[:8]
        self._created_at = created_at or datetime.now().isoformat()

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> str:
        return self._created_at

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to a dictionary for serialization."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        """Create an entity from a dictionary."""
        pass


class Task(Entity):
    def __init__(self, title: str, is_completed: bool = False, **kwargs):
        super().__init__(kwargs.get("id"), kwargs.get("created_at"))
        self._title = title
        self._is_completed = is_completed

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    def mark_complete(self):
        self._is_completed = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "title": self.title,
            "is_completed": self.is_completed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        return cls(
            title=data["title"],
            is_completed=data["is_completed"],
            id=data["id"],
            created_at=data["created_at"]
        )


class Project(Entity):
    def __init__(self, title: str, **kwargs):
        super().__init__(kwargs.get("id"), kwargs.get("created_at"))
        self._title = title
        self._tasks: List[Task] = kwargs.get("tasks") or []

    @property
    def title(self) -> str:
        return self._title

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def add_task(self, task_title: str) -> Task:
        new_task = Task(task_title)
        self._tasks.append(new_task)
        return new_task

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "title": self.title,
            "tasks": [task.to_dict() for task in self._tasks]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            title=data["title"],
            id=data["id"],
            created_at=data["created_at"],
            tasks=tasks
        )


class User(Entity):
    def __init__(self, name: str, **kwargs):
        super().__init__(kwargs.get("id"), kwargs.get("created_at"))
        self._name = name
        self._projects: List[Project] = kwargs.get("projects") or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def projects(self) -> List[Project]:
        return self._projects

    def add_project(self, project_title: str) -> Project:
        new_project = Project(project_title)
        self._projects.append(new_project)
        return new_project

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "name": self.name,
            "projects": [project.to_dict() for project in self._projects]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return cls(
            name=data["name"],
            id=data["id"],
            created_at=data["created_at"],
            projects=projects
        )
