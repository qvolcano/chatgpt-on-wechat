from PyOfficeRobot.core.WeChatType import *
from threading import Timer
from manager import ServiceManager
import pythoncom
import time
class Service():
    chats={}
    sendMessageQueue=[]
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
            for i in newest:
                info = self.parseMessage(i)
                ServiceManager.get("Action").run("_chat_handler",{'query'=info['content'],'context':info]})
        sendMessageQueue=self.sendMessageQueue.copy()
        for i in sendMessageQueue:
            target = i['target']
            self.wx.ChatWith(target)
            self.wx.sendMessage(i['content'])
        self.sendMessageQueue.clear()
        self.timer.start()
     def sendMessage(self,content):
        self.sendMessageQueue.append(content)
        pass
     def parseMessage(self,content):
        info = {}
        if content.startWish("@") :
            split = content.index(" ")
            info['target']=content[1:split]
            info['content]=content[split:]
        else:
            info['content']=content
        return info

class Chat():
    lastChatTime=0
    def getNewMessages(self,messages):
        newets=[]
        for i in messages:
            if int(i[2])>self.lastChatTime:
                newets.append(i)
        return newets

default = Service
