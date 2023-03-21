
# encoding:utf-8

"""
wechat channel
"""
import itchat
import json
from itchat.content import *
from concurrent.futures import ThreadPoolExecutor
from common.log import logger
from common.tmp_dir import TmpDir
from manager import ServiceManager
from manager import ActionManager
from manager import PrivoderManager
import asyncio
import requests
import io

permission = ["system"]


class Service():
    def start(self):
        pass
    def stop(self):
        pass
    def handle(self, msg):
        logger.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
        from_user_id = msg['FromUserName']
        to_user_id = msg['ToUserName']              # 接收人id
        other_user_id = msg['UserName']     # 对手方id
        content = msg['Text']
        self._do_send_text(content, to_user_id, msg)

    def build_reply_content(self, query, context):
        return asyncio.run(ActionManager.run_async("_chat", {"query": query, "context": context}, "system"))

    def _do_send_text(self, query, reply_user_id, msg):
        try:
            if not query:
                return
            context = dict()
            context['from_user_id'] = reply_user_id
            for i in msg:
                context[i] = msg[i]
            reply_text = self.build_reply_content(query, context)
            if reply_text:
                ServiceManager.get("WechatWinService").send(reply_text, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def _do_send_img(self, query, reply_user_id, msg):
        try:
            if not query:
                return
            context = dict()
            context['type'] = 'IMAGE_CREATE'
            for i in msg:
                context[i] = msg[i]
            img_url = self.build_reply_content(query, context)
            if not img_url:
                return

            # 图片下载
            pic_res = requests.get(img_url, stream=True)
            image_storage = io.BytesIO()
            for block in pic_res.iter_content(1024):
                image_storage.write(block)
            image_storage.seek(0)

            # 图片发送
            logger.info('[WX] sendImage, receiver={}'.format(reply_user_id))
            itchat.send_image(image_storage, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def check_prefix(self, content, prefix_list):
        for prefix in prefix_list:
            if content.startswith(prefix):
                return prefix
        return None

    def check_contain(self, content, keyword_list):
        if not keyword_list:
            return None
        for ky in keyword_list:
            if content.find(ky) != -1:
                return True
        return None


    def sendMessage(self,message,reply):
        ServiceManager.get("WechatWinService").send(message, reply)

default = Service
