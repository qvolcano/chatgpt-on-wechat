from PyOfficeRobot.core.WeChatType import *
from threading import Timer
from manager import ServiceManager
from manager import PrivoderManager
import pythoncom
import time
class Service():
    chats={}
    chatsHistory={}
    send_message_queue = []
    def start(self):
        # 获取当前微信客户端
        self.wx = WeChat()
        self.timer = Timer(1,self.tick)
        self.timer.start()
        self.startTime=time.time()
        self.lastTickTime=time.time()
    def stop(self):
        self.timer.cancel()
    def send(self,content,to_user):
        self.send_message_queue.append({'content':content,'ToUserName':to_user})
    def tick(self):
        print("tick")
        self.timer.cancel()
        pythoncom.CoInitialize()
        sessionlist=["狗蛋"] or PrivoderManager.get("config").get("chat_whitelist") or self.wx.GetSessionList(True)
        #check new
        for i in sessionlist:
            self.wx.ChatWith(i)
            try:
                messages=self.wx.GetAllMessage
                lastMessages=messages[-10:]
                lastMessage=self.wx.GetLastMessage
                if self.chatsHistory.get(i)==None:
                    self.chatsHistory[i]=messages[-10:]
                else:
                    #get news
                    history=self.chatsHistory[i]
                    last_history_chat=history[-1]
                    history_count = len(history)
                    new_messages = None
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
                        new_messages=messages[max_seq_index:]
                        for l in range(max_seq_index,len(messages)):
                            message=messages[l]
                            msg={}
                            msg['FromUserName'] = message[0]
                            msg['ToUserName'] = message[0] #check @
                            msg['UserName'] = message[0]
                            item=self.wx.MsgList.GetChildren()[l]
                            if len(item.GetChildren()[0].GetChildren())>0:
                                if item.GetChildren()[0].GetChildren()[0].LocalizedControlType=="按钮":
                                    msg['FromUserName'] = item.GetChildren()[0].GetChildren()[0].Name
                                    #别人的发言
                                    pass
                                else:
                                    #自己的发言
                                    msg['FromUserName'] = item.GetChildren()[0].GetChildren()[2].Name
                                    msg["self"]=True
                                msg["Text"]=message[1]
                                # to_user_id = msg['ToUserName']              # 接收人id
                                # other_user_id = msg['User']['UserName']     # 对手方id
                                # content = msg['Text']
                                ServiceManager.get("ChatBotService").handle(msg)
                        # self.chatsHistory[i]=lastMessage[2]
            except Exception as e:
                print(e)
        if len(self.send_message_queue)>0:
            for i in self.send_message_queue:
                self.wx.ChatWith(i['ToUserName'])
                self.wx.SendMsg(i['context'])
            self.send_message_queue=[]

        self.timer = Timer(1,self.tick)
        self.timer.start()

# def get_max_same(lista,listb,check):



default = Service