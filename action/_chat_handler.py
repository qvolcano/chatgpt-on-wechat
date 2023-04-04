
# encoding:utf-8

"""
wechat channel
"""
import json
from concurrent.futures import ThreadPoolExecutor
from common.log import logger
from common.tmp_dir import TmpDir
from manager import ServiceManager
from manager import ActionManager
from manager import PrivoderManager
from manager import PermissionManager
import asyncio
import io

permission = ["system"]

async def default( msg):
    logger.info("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    from_user_id = msg['FromUserName']
    to_user_id = msg['ToUserName']              # 接收人id
    other_user_id = msg['UserName']     # 对手方id
    content = msg['Text']
    await _do_send_text(content, to_user_id, msg)

async def build_reply_content( query, context):
    if query.startswith("/"):
        split=query.find(" ")
        if split>=0 :
            name=query[1:split]
            query=query[split+1:]
        else:
            name=query[1:]
        ##check Permission
        user=context["FromUserName"]
        context['query']=query
        return await ActionManager.run_async(name,context,user=user)
    return await ActionManager.run_async("chat_receive", context, "system")

async def _do_send_text( query, reply_user_id, msg):
    try:
        if not query:
            return
        context = dict()
        context['from_user_id'] = reply_user_id
        for i in msg:
            context[i] = msg[i]
        session=context['session']
        logger.info("[WX]received msg: " + query)
        ServiceManager.get("WechatWinService").send("正在查询，请稍后",session, reply_user_id)
        reply_text = await build_reply_content(query, context)
        if reply_text:
            ServiceManager.get("WechatWinService").send(reply_text,session, reply_user_id)
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


def sendMessage(message,reply):
    ServiceManager.get("WechatWinService").send(message, reply)
