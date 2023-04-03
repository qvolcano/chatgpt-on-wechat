# encoding:utf-8
import config
from common.log import logger
from manager import ServiceManager
from manager import ActionManager
from manager import TaskManager
from manager import PrivoderManager
from manager import PermissionManager
import time
import asyncio
import threading
def start():
    pass
if __name__ == '__main__':
    try:
        thread_loop = asyncio.new_event_loop()
        ActionManager.setup(thread_loop)
        config.load_config()
        for i  in config.config.get("admin"):
            PermissionManager.setUserGroup(i,"admin")

        PrivoderManager.set("config",config.config)
        # ServiceManager.add("WechatService")
        ServiceManager.add("OpenaiService")
        ServiceManager.add("ChatBotService")
        # ServiceManager.add("BingService")
        ServiceManager.add("WechatWinService")
        ServiceManager.start("ChatBotService")

        # ServiceManager.start("WechatService")
        ServiceManager.start("OpenaiService")
        ServiceManager.start("WechatWinService")
        thread_loop.run_forever()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)