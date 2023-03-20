from EdgeGPT import Chatbot as EdgeChatbot, ConversationStyle
from manager import PrivoderManager
import asyncio
import re
import json
import os
class Service:
    def start(self):
        self.bing_api_key=PrivoderManager.get("config").get("bing_api_key")
        # self.bot = EdgeChatbot("cookie.json")
        self.bot = EdgeChatbot("",[{
            "name":"_U",
            "value":self.bing_api_key
        }])
        self.conversation_style = ConversationStyle.creative
    def stop(self):
        self.bot.close()
        pass
    def reply(self, query, context=None):
        result = ""
        async def post():
            resp=await self.bot.ask(prompt=query, conversation_style=ConversationStyle.creative)
            #return str(resp)
            message=resp['item']['messages'][1]
            result = message['text']
            return message['text']
        get_future = asyncio.ensure_future(post()) # 相当于开启一个future
        asyncio.get_event_loop().run_until_complete(get_future) # 事件循环
        return get_future.result()
default = Service
