# Advanced Project Tracker CLI

A project management Command-Line Interface (CLI) application built with Python. This project demonstrates high-level software architecture, object-oriented design, and robust data persistence.

## 🚀 Key Features

- **Multi-User Support**: Assign projects and tasks to specific users with a clear one-to-many relationship.
- **Robust Persistence**: Local JSON-based storage with comprehensive error handling (IO, Permission, Corruption).
- **Advanced OOP Design**: 
  - Abstract Base Class (`Entity`) for consistent structure across all models.
  - Encapsulation using private attributes and `@property` decorators.
  - Custom serialization (`to_dict`/`from_dict`) for deeply nested data structures.
- **Professional CLI**: 
  - Powered by `argparse` with modular subparsers.
  - Visually rich output using the `rich` library (tables, panels, status colors).
  - Global exception handling to provide a user-friendly experience.
- **Input Validation**: Schema-based validation using `pydantic`.
- **Date Formatting**: Human-readable creation dates using `python-dateutil`.
- **Comprehensive Testing**: 100% logic coverage with `pytest` and mocked storage layers.

## 🛠 Modular Architecture

The codebase is strictly organized to ensure clear separation of concerns:

- `src/models.py`: Core domain models (`User`, `Project`, `Task`) and OOP logic.
- `src/storage.py`: Data persistence, serialization, and file I/O error handling.
- `src/cli.py`: CLI subcommands, `argparse` setup, and visual formatting.
- `src/utils.py`: Reusable helper functions and logging configuration.
- `main.py`: Application entry point.
- `tests/test_app.py`: Full test suite for validating all application logic.

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- `pipenv` (recommended) or `pip`

### Install Dependencies
Using Pipenv:
```bash
pipenv install
```

Or using pip:
```bash
pip install rich pydantic python-dateutil pytest
```

## 🎮 Usage

### Add a New User
```bash
python main.py add-user --name "Alice"
```

### Add a Project to a User
```bash
python main.py add-project --user "Alice" --title "Website Redesign"
```

### Add a Task to a Project
```bash
python main.py add-task --project "Website Redesign" --title "Create Mockups"
```

### Mark a Task as Complete
```bash
python main.py complete-task --task-id <TASK_ID>
```

### View Dashboard
```bash
python main.py list
```

## 🧪 Testing

To run the test suite:
```bash
python -m pytest tests/test_app.py
```

## 📝 Logging

The application maintains a debug log in `app.log`, capturing all operations and errors for troubleshooting.

---
*Developed on June 16th, 2026*
