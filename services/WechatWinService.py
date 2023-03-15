from PyOfficeRobot.core.WeChatType import *
from threading import Timer
import pythoncom
import time
class Service():
    chats={}
    def start(self):
        # 获取当前微信客户端
        self.wx = WeChat()
        self.timer = Timer(1,self.tick)
        self.timer.start()
    def stop(self):
        self.timer.cancel()

    def tick(self):
        self.timer.cancel()
        pythoncom.CoInitialize()
        sessionlist=self.wx.GetSessionList()
        #check new
        self.wx.time
        for i in sessionlist:
            if self.chats.get(i)==None:
                self.chats[i]=Chat()
                self.chats[i].setLastChatTime(sessionlist)
            self.wx.ChatWith(i)
            self.wx.UiaAPI
            messages=self.wx.GetAllMessage
            newest=self.chats[i].getNewMessages(messages)
            self.chats[i].lastChatTime=messages[-1]
        self.timer.start()

class Chat():
    lastChatTime=0
    def getNewMessages(self,messages):
        newets=[]
        for i in messages:
            if int(i[2])>self.lastChatTime:
                newets.append(i)
        return newets

default = Service