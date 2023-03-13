from manager import ServiceManager
from manager import ActionManager
from manager import PermissionManager
import traceback
permission=(
    "admin"
)

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
        for i in context.get("User")['MemberList']:
            if context['FromUserName'] == i['UserName']:
                user=context.get("User")["NickName"]
                permission=PermissionManager.getUserGroup(user)
        return ActionManager.run(name,args,permission=permission)
    else:
        return ServiceManager.get("OpenaiService").reply(query, context)
    # ServiceManager.get("OpenaiService").reply()
