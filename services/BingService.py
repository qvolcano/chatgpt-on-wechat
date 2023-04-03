from manager import PrivoderManager
import asyncio
import re
import json
import os
class Service:
    def start(self):
        self.bing_api_key=PrivoderManager.get("config").get("bing_api_key")
        # self.bot = EdgeChatbot("cookie.json")
        
    def stop(self):
        pass
    async def reply(self, query, context=None):
        return 
default = Service
