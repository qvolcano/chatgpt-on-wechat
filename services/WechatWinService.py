from PyOfficeRobot.core.WeChatType import *
from threading import Timer
from threading import Thread
from manager import ServiceManager
from manager import PrivoderManager
from manager import ActionManager

from common.log import logger
import pythoncom
import time
import asyncio
import pyautogui

class RepeatTimer (Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args,**self.kwargs)
            self.finished.wait(self.interval)
class Service():
    chats={}
    chatsHistory={}
    send_message_queue = []
    def start(self):
        # 获取当前微信客户端
        self.wx = WeChat()
        self.timer = RepeatTimer(1,self.tick_time)
        self.startTime=time.time()
        self.lastTickTime=time.time()
        self.wx.MsgList.GetPreviousSiblingControl()
        self.session_check_queue=[]
        self.session_news={}
        try:
            self.user_name=self.wx.UiaAPI.ButtonControl(Name="聊天").GetPreviousSiblingControl().Name
        except:
            self.user_name = ""
        for i in self.wx.GetSessionList():
            self.session_check_queue.append(i)
        pythoncom.CoInitialize()
        self.timer.start()

    def stoptimer(self,event):
        self.timer.cancel()

    def tick_time(self):
        self.queue_check_session()
        self.queue_update_chat()
        self.queue_send_chat()
        
    def queue_check_session(self):
        try:
            redots=pyautogui.locateOnWindow("./imgs/picture4.png",confidence=0.9,title="微信")
            if redots :
                redots=list(redots)
                if len(redots):
                    print(redots)
                    sessions=self.wx.SessionList.GetChildren()
                    for i in sessions:
                        has_redot=False
                        if len(i.GetChildren()[0].GetChildren())==3:
                            has_redot=True
                        if has_redot:
                            self.session_check_queue.append(i.Name)
        except:
            pass
                
    def queue_update_chat(self):
        self.session_check_queue=list(set(self.session_check_queue))
        for i in self.session_check_queue:
            self.update_chat2(i)
            time.sleep(0.1)
        self.session_check_queue=[]
            
    def queue_send_chat(self):
        if self.wx.UiaAPI.IsMinimize():
            self.wx.UiaAPI.SwitchToThisWindow()
        for i in self.send_message_queue:
            try:
                uia.SendKeys('{Ctrl}a', waitTime=0,)
                WxUtils.SetClipboard(i['content'])
                uia.SendKeys('{Ctrl}v', waitTime=0,)
                pyautogui.press("enter")
            except:
              pass
            self.session_check_queue.append(i['session'])
        self.send_message_queue=[]

            
   
        
    def stop(self):
        self.timer.cancel()
    def send(self,content,session,to_user):
        logger.info("inster send"+str(len(self.send_message_queue)))
        self.send_message_queue.append({'content':content,'session':session,'ToUserName':to_user})
    def update_chat2(self,session):
        self.ChatWith(session)
        try:
            messages=self.wx.GetAllMessage
            lastMessages=messages[-10:]

            if self.chatsHistory.get(session)==None:
                self.chatsHistory[session]=messages[-10:]
            else:

                #get news
                history=self.chatsHistory[session]
                if len(self.wx.UiaAPI.GetChildren())==3:
                    session_names=get_ui_by_childs(self.wx.UiaAPI,[2,1,2,0,0,0,0,0,0,1,0,0,0]).GetChildren()

                else:
                    session_names=get_ui_by_childs(self.wx.UiaAPI,[1,1,2,0,0,0,0,0,0,1,0,0,0]).GetChildren()
                session_title_name = session_names[0].Name
                session_num=""
                if len(session_names)>1:
                    session_num = session_names[1].Name[2:-1]
                is_group_chat=False
                if session_num!="":
                    is_group_chat=True
                max_seq_index=-1
                max_seq_nums=0
                for l in range(len(messages)-1,max(len(messages)-30-1,-1),-1):
                    seq_nums = 0
                    for i in range(len(history)-1,-1,-1):
                        ch=history[i]
                        if ch[1]==messages[l-(len(history)-1-i)][1]:
                            seq_nums=seq_nums+1
                        else:
                            if seq_nums>max_seq_nums:
                                max_seq_nums =seq_nums
                                max_seq_index=l+1
                            break
                    if seq_nums == len(history):
                        max_seq_index = l +1
                        break
                if max_seq_index!=-1:
                    for l in range(max_seq_index,len(messages)):
                        message=messages[l]
                        msg={}
                        self.wx.UiaAPI.WindowControl()
                        msg['session'] = session
                        msg['FromUserName'] = message[0]
                        msg['ToUserName'] = message[0] #check @
                        msg['UserName'] = message[0]
                        msg['is_group_chat'] = is_group_chat
                        msg["self"]=False
                        item=self.wx.MsgList.GetChildren()[l]
                        if len(item.GetChildren()[0].GetChildren())>0:
                            if item.GetChildren()[0].GetChildren()[0].LocalizedControlType=="按钮":
                                msg['FromUserName'] = item.GetChildren()[0].GetChildren()[0].Name
                                #别人的发言
                                pass
                            else:
                                #自己的发言么我能帮忙解答的问题吗？
                                msg['FromUserName'] = item.GetChildren()[0].GetChildren()[2].Name
                                msg["self"]=True
                            msg["Text"]=message[1] or ""
                            if is_group_chat:
                            
                                if msg["Text"].startswith("@"):
                                    ToUserName=msg['Text'][1:msg['Text'].find("\u2005")]
                                    msg['ToUserName']=ToUserName
                                    if ToUserName == self.user_name:
                                        ActionManager.run("_chat_handler",msg)
                            else:
                                #私聊
                                if msg.get('self')==False:
                                    ActionManager.run("_chat_handler",msg)
                    self.chatsHistory[session]=messages[-10:]
                    logger.info("update_chat2")

        except Exception as e:
            print(e)

    def ChatWith(self, who, RollTimes=None):
        if self.wx.UiaAPI.IsMinimize() :
            self.wx.UiaAPI.SwitchToThisWindow()
        item=self.wx.SessionList.ListItemControl(Name=who)
        item.MoveCursorToInnerPos()
        time.sleep(0.1)
        item.Click(simulateMove=False,waitTime=0)
def change_lang(lang):
    from win32con import WM_INPUTLANGCHANGEREQUEST
    import win32gui
    import win32api

    hwnd = win32gui.GetForegroundWindow()

    if lang == 'EN':
        ID = 0x0409
    # elif lang=='zh-CN':
    #     ID=0x0804
    elif lang == 'zh-TW':
        ID = 0x0404
    else:
        print('未知的語言類型')
        return

    win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, ID)

def get_ui_by_childs(root,childs):
    node=root
    for i in childs:
        node=node.GetChildren()[i]
    return node

default = Service
