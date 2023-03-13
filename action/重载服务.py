from manager import ServiceManager
def default(args):
  query=args['query']
  query.split(" ")
  if ServiceManager.status(query[1]) == "none":
    return "服务不存在"
  ServiceManager.stop(query[1])
  ServiceManager.start(query[1])
  return "服务"+query[1]+"重载完毕"
