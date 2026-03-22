import json, os
from datetime import datetime

DB = "tasks.json"

def load():
    if os.path.exists(DB):
        f = open(DB, "r")
        data = json.load(f)
        f.close()
        return data
    return []

def save(tasks):
    f = open(DB, "w")
    json.dump(tasks, f)
    f.close()

def add_task(title, priority="medium"):
    tasks = load()
    t = {"id": len(tasks)+1, "title": title, "priority": priority, "done": False, "created": str(datetime.now())}
    tasks.append(t)
    save(tasks)
    print(f"added: {title}")

def complete_task(task_id):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            print(f"completed: {t['title']}")
            return
    print("task not found")

def delete_task(task_id):
    tasks = load()
    new = []
    for t in tasks:
        if t["id"] != task_id:
            new.append(t)
    save(new)
    print("deleted")

def list_tasks(show_done=False):
    tasks = load()
    for t in tasks:
        if not show_done and t["done"]:
            continue
        status = "DONE" if t["done"] else "PENDING"
        print(f"[{t['id']}] {t['title']} - {t['priority']} - {status}")

def search(keyword):
    tasks = load()
    results = []
    for t in tasks:
        if keyword.lower() in t["title"].lower():
            results.append(t)
    return results

if __name__ == "__main__":
    add_task("Write unit tests", "high")
    add_task("Update README")
    add_task("Fix login bug", "high")
    list_tasks()
    complete_task(1)
    list_tasks(show_done=True)
    print(search("test"))
