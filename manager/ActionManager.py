import importlib
import traceback
import sys
def setup():
    pass

def run(name,args,permission=None,userGroup=None):
    try:
        class_path="action."+name
        if sys.modules.get(class_path):
            del sys.modules[class_path]
        action=importlib.import_module(class_path)
        # importlib.reload(action)
        permission= None
        try:
            permission =action.permission
        except:
            permission= None
            pass
        userGroup=userGroup or "guest"
        if permission :
            find=False
            for i in permission:
                if i == userGroup:
                    find = True
                    break
            if not find:
                return "没有权限"
        resp = action.default(args)
        del sys.modules[class_path]
        return resp
    except  Exception as e:
        print(traceback.format_exc())
        return "error" 
