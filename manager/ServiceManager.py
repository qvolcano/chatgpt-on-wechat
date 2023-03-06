import importlib
import sys
def setup():
    pass

services={}
def add(class_path):
    services[class_path]={
        "class_path":class_path,
        "service":None
    }

def start(name):
    info=services[name]
    if info :
        if info['service']==None:
            info['service']=_create(name)
            info['service'].start()
def stop(name):
    info=services[name]
    if info :
        if info['service']:
            del sys.modules['service']
            del info['service']
def _create(name):
    info=services[name]
    class_path=info['class_path']
    service=importlib.import_module(class_path)
    return service