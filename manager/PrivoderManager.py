datas={}
def set(key,value):
    datas[key]=value
def get(key):
    return datas[key]
def setValue(sheet,key,value):
    data=datas.get(sheet)
    if data:
        data.set(key,value)

import json
import os
class JsonProvider():
    def __init__(self,path) -> None:
        self.path=path
        self.src=json.load(path)
    def get(self,key):
        return self.src.get(key)
    def set(self,key,value):
        self.src[key]=value
        self.flush()
    def flush(self):
        json.dump(self.src,self.path)
