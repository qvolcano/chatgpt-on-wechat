import importlib
import threading
def main():
    pass

tasks={}

def run(class_path):
    class_path="tasks."+class_path
    if tasks.get(class_path) != None:
        print("重复任务")
        return 1
    try:
        task=importlib.import_module(class_path)
        
        # task=Task("tasks."+class_path)
        tasks[class_path] =threading.Thread(target=_task,args=(class_path,task))
        tasks[class_path].start()
        # task.start()
        return 0
    except:
        return -1

def _task(class_path,task):
    task.default()
    del tasks[class_path]