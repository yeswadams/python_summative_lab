import pytest
import os
import json
from src.models import User, Project, Task
from src.storage import Storage

@pytest.fixture
def mock_storage(tmp_path):
    """Fixture to provide a Storage instance pointed at a temporary file."""
    db_file = tmp_path / "test_storage.json"
    return Storage(str(db_file))

def test_user_creation():
    user = User(name="Alice")
    assert user.name == "Alice"
    assert user.id is not None
    assert len(user.projects) == 0

def test_project_addition():
    user = User(name="Alice")
    project = user.add_project("CLI App")
    assert len(user.projects) == 1
    assert user.projects[0].title == "CLI App"
    assert project.title == "CLI App"

def test_task_addition():
    project = Project(title="CLI App")
    task = project.add_task("Implement models")
    assert len(project.tasks) == 1
    assert project.tasks[0].title == "Implement models"
    assert not task.is_completed

def test_task_completion():
    task = Task(title="Implement models")
    task.mark_complete()
    assert task.is_completed

def test_storage_save_load(mock_storage):
    users = {"Alice": User(name="Alice")}
    users["Alice"].add_project("CLI App").add_task("Implement models")
    
    mock_storage.save_data(users)
    loaded_users = mock_storage.load_data()
    
    assert "Alice" in loaded_users
    assert len(loaded_users["Alice"].projects) == 1
    assert loaded_users["Alice"].projects[0].title == "CLI App"
    assert len(loaded_users["Alice"].projects[0].tasks) == 1
    assert loaded_users["Alice"].projects[0].tasks[0].title == "Implement models"

def test_storage_corrupted_file(tmp_path):
    db_file = tmp_path / "corrupted.json"
    with open(db_file, "w") as f:
        f.write("invalid json")
    
    storage = Storage(str(db_file))
    data = storage.load_data()
    assert data == {}

def test_to_from_dict_serialization():
    user = User(name="Bob")
    project = user.add_project("Web App")
    task = project.add_task("Setup server")
    
    user_dict = user.to_dict()
    new_user = User.from_dict(user_dict)
    
    assert new_user.name == "Bob"
    assert len(new_user.projects) == 1
    assert new_user.projects[0].title == "Web App"
    assert new_user.projects[0].tasks[0].title == "Setup server"
    assert new_user.id == user.id
    assert new_user.created_at == user.created_at
