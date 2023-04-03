import importlib
import traceback
import sys
import asyncio
cache={}
_thread_loop = asyncio.get_event_loop()

def reload():
    for i in cache:
        importlib.reload(cache[i])

def create_action(name):
    class_path="action."+name
    if cache.get(class_path) == None:
        mod=importlib.import_module(class_path)
        try:
            cache[class_path]=mod
            return mod.default
        except:
            return mod
    return cache[class_path].default

def setup(thread_loop):
    global _thread_loop
    _thread_loop=thread_loop
    pass
def run(name,args,user=None):
    try:
        asyncio.run_coroutine_threadsafe(run_async(name,args,user),_thread_loop)
    except Exception as e:
        asyncio.run(run_async(name,args,user))

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
            if asyncio.iscoroutinefunction(action):
                return await action(args)
            else:
                return action(args)
        except:
            raise Exception("执行错误")
