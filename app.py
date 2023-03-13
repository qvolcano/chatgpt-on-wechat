# encoding:utf-8

import config
from channel import channel_factory
from common.log import logger
from manager import ServiceManager
from manager import ActionManager
from manager import TaskManager
from manager import PrivoderManager
from manager import PermissionManager
import time
# import os
# import json
import asyncio
def test():
    print(1)
    print(2)
    return 4
if __name__ == '__main__':
    try:
        config.load_config()
        channel = channel_factory.create_channel("wx")
        config.load_config()
        for i  in config.config.get("admin"):
            PermissionManager.setUserGroup(i,"admin")
        PrivoderManager.set("config",config.config)
        ServiceManager.add("WechatService")
        ServiceManager.add("OpenaiService")
        ServiceManager.add("BingService")
        ServiceManager.start("WechatService")
        ServiceManager.start("BingService")
        ServiceManager.start("OpenaiService")
        ServiceManager.get("WechatService").login()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)
# import asyncio
# import time
# async def get_html(url):
#     return 4
# def callback(url, future):
#     print(url)
#     print("send email to bobby")
# if __name__ == "__main__":
#     start_time = time.time()
#     loop = asyncio.get_event_loop()
#     get_future = asyncio.ensure_future(get_html("http://www.imooc.com")) # 相当于开启一个future
#     loop.run_until_complete(get_future) # 事件循环
#     print(get_future.result()) # 获取结果