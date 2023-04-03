# from concurrent.futures import ThreadPoolExecutor
# import time


# def test(t):
#     time.sleep(1)
#     print(t)
# thread_pool = ThreadPoolExecutor(max_workers=8)
# thread_pool.submit(test,1)
# thread_pool.submit(test,2)
# thread_pool.submit(test,3)
# thread_pool.submit(test,4)
# thread_pool.submit(test,5)
# thread_pool.submit(test,6)
# thread_pool.submit(test,7)


# encoding:utf-8

import config
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
import threading
def start():
    print(1)
    print(2)
    return 4
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
        # ServiceManager.get("WechatService").login()
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

# # import asyncio
# # async def test(s):
# #     print(s)
# #     return 2

# # async def test2():
# #     await asyncio.coroutine(test)(4)
# # asyncio.run(test2())


# # from wcferry import Wcf

# # wcf = Wcf()
# # wcf.is_login()
# # wcf

# a = [1,2,3,4,5,6,7,8]
# for k in ra(10,1):
#     print(k)

# import asyncio
# import time

# async def test():
#     time.sleep(1)
#     print(1)
# asyncio.ensure_future(test())
# # run_forever(test())
# print(2)
# asyncio.get_event_loop().run_forever()
# # asyncio.create_task(test())