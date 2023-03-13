from manager import ServiceManager
from manager import ActionManager
from manager import PermissionManager
from manager import PrivoderManager
import traceback
permission=["admin"]

def default(args):
    context=args['context']
    query=args['query']
    if context!=None and context.get('MsgType') == 34 :
        return ServiceManager.get("OpenaiService").reply_sound(context, context)
    if query.startswith("/") :
        split=query.find(" ")
        if split>=0 :
            name=query[1:split]
            query=query[split+1:]
        else:
            name=query[1:]
        ##check Permission
        permission=None
        if len(context.get("User")['MemberList'])>0:
            for i in context.get("User")['MemberList']:
                print(i)
                if context['FromUserName'] == i['UserName']:
                    user=i["NickName"]
                    permission=PermissionManager.getUserGroup(user)
        else:
            user=context.get("User")["NickName"]
            permission=PermissionManager.getUserGroup(user)
        return ActionManager.run(name,args,userGroup="admin")
    else:
        chat_ai=PrivoderManager.get("config").get("chat_ai")
        if chat_ai == "bing":
            ServiceManager.start("BingService")
            return ServiceManager.get("BingService").reply(query, context)
        return ServiceManager.get("OpenaiService").reply(query, context)
    # ServiceManager.get("OpenaiService").reply()
