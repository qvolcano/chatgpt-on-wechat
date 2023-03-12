from manager import PrivoderManager
from manager import ServiceManager

def default(name,args):
    query=args.get("query")
    params=query.split(" ")
    if params[1] == "openai":
        if ServiceManager.status("OpenaiService")=="stop":
            ServiceManager.start("OpenaiService")
    if params[1] == "bing":
        if ServiceManager.status("BingService")=="stop":
            ServiceManager.start("BingService")
        PrivoderManager.get("config")['chat_ai']="bing"