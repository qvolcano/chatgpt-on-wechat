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
from config import conf
from manager import ServiceManager
from manager import ActionManager
import asyncio
import requests
import io

permission=["system"]
def default(msg):
    logger.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    from_user_id = msg['FromUserName']
    to_user_id = msg['ToUserName']              # 接收人id
    other_user_id = msg['User']['UserName']     # 对手方id
    content = msg['Text']
    match_prefix = check_prefix(content, conf().get('single_chat_prefix'))
    if "」\n- - - - - - - - - - - - - - -" in content:
        logger.debug("[WX]reference query skipped")
        return
    if from_user_id == other_user_id and match_prefix is not None:
        # 好友向自己发送消息
        if match_prefix != '':
            str_list = content.split(match_prefix, 1)
            if len(str_list) == 2:
                content = str_list[1].strip()

        img_match_prefix = check_prefix(content, conf().get('image_create_prefix'))
        if img_match_prefix:
            content = content.split(img_match_prefix, 1)[1].strip()
            _do_send_img(content, from_user_id, msg)
        else:
            _do_send_text(content, from_user_id, msg)

    elif to_user_id == other_user_id and match_prefix:
        # 自己给好友发送消息
        str_list = content.split(match_prefix, 1)
        if len(str_list) == 2:
            content = str_list[1].strip()
        img_match_prefix = check_prefix(content, conf().get('image_create_prefix'))
        if img_match_prefix:
            content = content.split(img_match_prefix, 1)[1].strip()
            _do_send_img(content, to_user_id, msg)
        else:
            _do_send_text(content, to_user_id, msg)

def build_reply_content(query,context):
    return asyncio.run(ActionManager.run_async("_chat",{"query":query,"context":context},"system"))

def _do_send_text( query, reply_user_id, msg):
    try:
        if not query:
            return
        context = dict()
        context['from_user_id'] = reply_user_id
        for i in msg:
            context[i] = msg[i]
        reply_text = build_reply_content(query, context)
        if reply_text:
            ServiceManager.get("WechatService").send(reply_text, reply_user_id)
    except Exception as e:
        logger.exception(e)

def _do_send_img( query, reply_user_id, msg):
    try:
        if not query:
            return
        context = dict()
        context['type'] = 'IMAGE_CREATE'
        for i in msg:
            context[i] = msg[i]
        img_url = build_reply_content(query, context)
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


def check_prefix( content, prefix_list):
    for prefix in prefix_list:
        if content.startswith(prefix):
            return prefix
    return None

def check_contain( content, keyword_list):
    if not keyword_list:
        return None
    for ky in keyword_list:
        if content.find(ky) != -1:
            return True
    return None