from bot import bot_factory
import manager.ActionManager as ActionManager
class Bridge(object):
    def __init__(self):
        pass

    def fetch_reply_content(query, context):
        if query.startswith("/") :
            split=query.find(" ")
            if split>=0 :
                name=query[1:split]
                query=query[split+1:]
            else:
                name=query[1:]
            return ActionManager.run(name,query,context)
        else:
            return bot_factory.create_bot("chatGPT").reply(query, context)
