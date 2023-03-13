import requests

def default(context):
    if len(context.get("User")['MemberList'])>0:
        for i in context.get("User")['MemberList']:
            return str(i)
    else:
        user=context.get("User")["NickName"]
        permission=PermissionManager.getUserGroup(user)
    return str(user)
