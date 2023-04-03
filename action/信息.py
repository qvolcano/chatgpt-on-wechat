import requests
from manager import PermissionManager
def default(args):
    context=args['context']
    if len(context.get("User")['MemberList'])>0:
        for i in context.get("User")['MemberList']:
            return str(i)
    else:
        user=context.get("User")["NickName"]
    return str(PermissionManager.getUserGroup(user))
