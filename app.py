# encoding:utf-8

import config
from channel import channel_factory
from common.log import logger
from manager import ServiceManager
from manager import ActionManager
from manager import TaskManager
from manager import PrivoderManager
from manager import PermissionManager

if __name__ == '__main__':
    try:
        # load config
        # config.load_config()
        # # create channel
        # channel = channel_factory.create_channel("wx")
        config.load_config()
        PermissionManager.setUserGroup("QV","admin")
        PrivoderManager.set("config",config.config)
        # # startup channel
        # channel.startup()
        ServiceManager.add("WechatService")
        ServiceManager.add("OpenaiService")
        ServiceManager.add("BingService")
        ServiceManager.start("WechatService")
        ServiceManager.start("OpenaiService")
        TaskManager.run("login")

    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)
