import importlib
import traceback
def setup():
    pass

def run(name,query,context):
    try:
        action=importlib.import_module("action."+name)
        return action.main(query,context)
    except  Exception as e:
        print(traceback.format_exc())
        return "error" 
