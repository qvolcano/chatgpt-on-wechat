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
            del sys.modules["services."+info['class_path']]
            del info['service']

def status(name):
    info=services.get(name)
    if info:
        if info.get("service")==None:
            return "stop"
        else:
            return "running"
    else:
        return "none"

def _create(name):
    info=services[name]
    class_path="services."+info['class_path']
    module=importlib.import_module(class_path)
    if module.default :
        return module.default()
    return module

def get(name):
    return services[name]['service']
