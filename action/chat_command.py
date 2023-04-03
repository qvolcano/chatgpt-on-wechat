async def default(args):
  permission=None
  user=args.get("FromUser")
  permission=PermissionManager.getUserGroup(user)
  return await ActionManager.run_async(name,args,userGroup="admin")
