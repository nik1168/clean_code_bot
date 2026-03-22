"""Simple JSON-backed task manager."""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict


DEFAULT_DB = Path("tasks.json")


@dataclass
class Task:
    """Single to-do item."""
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    created: str = field(default_factory=lambda: datetime.now().isoformat())


class TaskStore:
    """Handles reading/writing tasks to a JSON file."""

    def __init__(self, path=DEFAULT_DB):
        self.path = path

    def load(self):
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [Task(**row) for row in json.load(f)]

    def save(self, tasks):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in tasks], f, indent=2)


class TaskManager:
    """CRUD operations on top of a TaskStore."""

    def __init__(self, store=None):
        self.store = store or TaskStore()

    def add(self, title, priority="medium"):
        """Create and persist a new task. Returns the task object."""
        tasks = self.store.load()
        next_id = max((t.id for t in tasks), default=0) + 1
        task = Task(id=next_id, title=title, priority=priority)
        tasks.append(task)
        self.store.save(tasks)
        return task

    def complete(self, task_id):
        """Mark a task as done. Raises ValueError if not found."""
        tasks = self.store.load()
        for t in tasks:
            if t.id == task_id:
                t.done = True
                self.store.save(tasks)
                return t
        raise ValueError(f"No task with id {task_id}")

    def delete(self, task_id):
        """Remove a task by id."""
        tasks = self.store.load()
        filtered = [t for t in tasks if t.id != task_id]
        if len(filtered) == len(tasks):
            raise ValueError(f"No task with id {task_id}")
        self.store.save(filtered)

    def list_tasks(self, include_done=False):
        tasks = self.store.load()
        if include_done:
            return tasks
        return [t for t in tasks if not t.done]

    def search(self, keyword):
        """Case-insensitive search on task titles."""
        kw = keyword.lower()
        return [t for t in self.store.load() if kw in t.title.lower()]


if __name__ == "__main__":
    mgr = TaskManager()

    mgr.add("Write unit tests", "high")
    mgr.add("Update README")
    mgr.add("Fix login bug", "high")

    print("-- pending --")
    for t in mgr.list_tasks():
        print(f"  [{t.id}] {t.title} ({t.priority})")

    mgr.complete(1)

    print("\n-- all tasks --")
    for t in mgr.list_tasks(include_done=True):
        tag = "x" if t.done else " "
        print(f"  [{tag}] {t.title} ({t.priority})")

    hits = mgr.search("test")
    print(f"\nsearch 'test': {[t.title for t in hits]}")
