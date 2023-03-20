import importlib
import traceback
import sys
import asyncio


class default():
    cache={}
    def reload(self,):
        for i in self.cache:
            importlib.reload(self.cache[i])

    def create_action(self,name):
        class_path="action."+name
        if self.cache[class_path] == None:
            mod=importlib.import_module(class_path)
            try:
                self.cache[class_path]=mod
                return mod.default
            except:
                return None
        return self.cache[class_path].default

    async def run_async(self,name,args,user=None):
        action = self.create_action(name)
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
