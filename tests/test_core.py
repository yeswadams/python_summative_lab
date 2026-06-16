import os
import pytest
from src.models import User, Project, Task
from src.storage_manager import StorageManager

@pytest.fixture
def temp_storage(tmp_path):
    """Generates an isolated temporary database path for testing data safely."""
    db_file = tmp_path / "test_storage.json"
    return StorageManager(filepath=str(db_file))

def test_object_relationships():
    user = User("Alex")
    project = user.add_project("CLI Engine")
    task = project.add_task("Write Tests")
    
    assert user.name == "Alex"
    assert len(user.projects) == 1
    assert user.projects[0].title == "CLI Engine"
    assert len(project.tasks) == 1
    assert task.is_completed is False
    
    task.mark_complete()
    assert task.is_completed is True

def test_persistence(temp_storage):
    users = {}
    alex = User("Alex")
    proj = alex.add_project("Lab Work")
    proj.add_task("Finish Code")
    users["Alex"] = alex
    
    # Save to mock temp location
    temp_storage.save_data(users)
    
    # Load back up to verify mirror consistency
    loaded_users = temp_storage.load_data()
    assert "Alex" in loaded_users
    assert loaded_users["Alex"].projects[0].title == "Lab Work"
    assert loaded_users["Alex"].projects[0].tasks[0].title == "Finish Code"