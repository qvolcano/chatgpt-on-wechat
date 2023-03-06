from bot import bot_factory
import manager.ActionManager as ActionManager
class Bridge(object):
    def __init__(self):
        pass

    def fetch_reply_content(self, query, context):
        print(context)
        print(context.get('type'))
        print(context.get('MsgType'))
        if context!=None and  context.get('MsgType') == 34 :
            return bot_factory.create_bot("chatGPT").reply_sound(context, context)
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
