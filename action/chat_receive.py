async def defaul(args):
  query=args.get("text")
  context=args
  chat_ai=PrivoderManager.get("config").get("chat_ai")
  if chat_ai == "bing":
    ServiceManager.start("BingService")
    return ServiceManager.get("BingService").reply(query, context)
  else:
    ServiceManager.start("OpenaiService")
    return await ServiceManager.get("OpenaiService").reply(query, context)
