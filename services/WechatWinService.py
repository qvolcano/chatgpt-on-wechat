from PyOfficeRobot.core.WeChatType import *
from threading import Timer
from threading import Thread
from manager import ServiceManager
from manager import PrivoderManager
from manager import ActionManager

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
        # keyboard.hook_key("f12",self.stoptimer)
        pythoncom.CoInitialize()
        # self.timer.daemon=False
        self.timer.start()
        # asyncio.get_event_loop().call_later(1,self.tick_time)

        # self.tick_time()

    def stoptimer(self,event):
        self.timer.cancel()

    def tick_time(self):
        self.queue_check_session()
        self.queue_update_chat()
        self.queue_send_chat()
        
    def queue_check_session(self):
        try:
            redots=pyautogui.locateOnWindow("./imgs/picture4.png",confidence=0.9,title="微信")
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
                # self.session_check_queue.append(i.Name)
        except:
            pass
                
    def queue_update_chat(self):
        self.session_check_queue=list(set(self.session_check_queue))
        for i in self.session_check_queue:
            if i=="腾讯新闻":
                continue
            self.update_chat2(i)
            time.sleep(0.1)
        self.session_check_queue=[]
            
    def queue_send_chat(self):
        for i in self.send_message_queue:
            self.ChatWith(i['session'])
            try:
                # self.wx.SendMsg(i['content'])
                self.wx.UiaAPI.SwitchToThisWindow()
                self.wx.EditMsg.SendKeys('{Ctrl}a', waitTime=0)
                WxUtils.SetClipboard(i['content'])
                self.wx.SendClipboard()
                # self.wx.EditMsg.SendKeys(msg, waitTime=0)
               # self.wx.EditMsg.SendKeys('{Enter}', waitTime=0)
            except:
              pass
            self.session_check_queue.append(i['session'])
        self.send_message_queue=[]

            
    def update_chat(self,session):
        self.wx.ChatWith(session)
        messages=self.wx.GetAllMessage
        if self.chatsHistory.get(session)==None:
            self.chatsHistory[session]=messages[-10:]
            self.session_news[session]=[]
        else:
            history=self.chatsHistory.get(session)
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
                self.session_news[session]=[]
        
        
    def stop(self):
        self.timer.cancel()
    def send(self,content,session,to_user):
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
                                    # else:
                                    #     ServiceManager.get("ChatBotService").handle(msg)
                                else:
                                    pass
                                   # if msg.get('self')==False:
                                      #  ActionManager.run("_chat_handler",msg)
                            else:
                                #私聊
                                if msg.get('self')==False:
                                    ActionManager.run("_chat_handler",msg)
                            # to_user_id = msg['ToUserName']              # 接收人id
                            # other_user_id = msg['User']['UserName']     # 对手方id
                            # content = msg['Text']

                        # self.chatsHistory[i]=lastMessage[2]
                    self.chatsHistory[session]=messages[-10:]


        except Exception as e:
            print(e)

    def ChatWith(self, who, RollTimes=None):
        '''
        打开某个聊天框
        who : 要打开的聊天框好友名，str;  * 最好完整匹配，不完全匹配只会选取搜索框第一个
        RollTimes : 默认向下滚动多少次，再进行搜索
        '''
        self.wx.UiaAPI.SwitchToThisWindow()
        time.sleep(0.5)
        self.wx.SessionList.ListItemControl(Name=who).Click(simulateMove=True)

def get_ui_by_childs(root,childs):
    node=root
    for i in childs:
        node=node.GetChildren()[i]
    return node
# def get_max_same(lista,listb,check):



default = Service
