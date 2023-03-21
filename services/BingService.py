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
    async def reply(self, query, context=None):
        return await self.bot.ask_stream(prompt=query, conversation_style=ConversationStyle.creative)
default = Service
