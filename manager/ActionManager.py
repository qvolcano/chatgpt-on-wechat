import importlib
import traceback
import sys
import asyncio
cache={}

def reload():
    for i in cache:
        importlib.reload(cache[i])

def create_action(name):
    class_path="action."+name
    if cache[class_path] == None:
        mod=importlib.import_module(class_path)
        try:
            cache[class_path]=mod
            return mod.default
        except:
            return None
    return cache[class_path].default

def setup():
    pass

async def run_async(name,args,user=None):
    action = create_action(name)
    if action !=None:
        permission= None
        try:
            permission =action.permission
        except:
            permission= None
            pass
        user=user or "guest"
        if permission :
            find=False
            for i in permission:
                if i == user:
                    find = True
                    break
            if not find:
                raise Exception("没有权限")
        try:
            return asyncio.coroutine(action)(args)
        except:
            raise Exception("执行错误")
    pass
