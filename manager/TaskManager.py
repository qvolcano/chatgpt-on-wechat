import importlib

def main():
    pass

tasks={}

class Task:
    class_path=None
    def __init__(self,class_path) -> None:
        self.class_path=class_path
        pass
    def start(self):
        task_execute=importlib.import_module(self.class_path)
        task_execute.default()
        pass

def run(class_path):
    task=Task("tasks."+class_path)
    task.start()
    return task