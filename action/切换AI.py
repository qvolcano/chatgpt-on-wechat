from manager import PrivoderManager
from manager import ServiceManager

def default(args):
    query=args.get("query")
    params=query.split(" ")
    if params[1] == "openai":
        if ServiceManager.status("OpenaiService")=="stop":
            ServiceManager.start("OpenaiService")
        PrivoderManager.get("config")['chat_ai']="openai"
        return "切换成功"
    if params[1] == "bing":
        if ServiceManager.status("BingService")=="stop":
            ServiceManager.start("BingService")
        PrivoderManager.get("config")['chat_ai']="bing"
        return "切换成功"