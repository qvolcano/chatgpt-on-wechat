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
        self.wx.MsgList.GetPreviousSiblingControl()
        try:
            self.user_name=self.wx.UiaAPI.ButtonControl(Name="聊天").GetPreviousSiblingControl().Name
        except:
            self.user_name = ""
    def stop(self):
        self.timer.cancel()
    def send(self,content,session,to_user):
        self.send_message_queue.append({'content':content,'session':session,'ToUserName':to_user})
    def tick(self):
        print("tick")
        self.timer.cancel()
        pythoncom.CoInitialize()
        sessionlist=["狗蛋、大姐儿子"] or PrivoderManager.get("config").get("chat_whitelist") or self.wx.GetSessionList(True)
        #check new
        
        for session in sessionlist:
            self.wx.ChatWith(session)
            try:
                messages=self.wx.GetAllMessage
                lastMessages=messages[-10:]

                lastMessage=self.wx.GetLastMessage
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
                                msg["Text"]=message[1] or ""
                                if is_group_chat:
                                    if msg["Text"].startswith("@"):
                                        ToUserName=msg['Text'][1:msg['Text'].find("\u2005")]
                                        msg['ToUserName']=ToUserName
                                        if session_names.find("群聊"):
                                            if ToUserName == self.user_name:
                                                ServiceManager.get("ChatBotService").handle(msg)
                                        # else:
                                        #     ServiceManager.get("ChatBotService").handle(msg)
                                    else:
                                        if msg['self']==False:
                                            ServiceManager.get("ChatBotService").handle(msg)
        
                                # to_user_id = msg['ToUserName']              # 接收人id
                                # other_user_id = msg['User']['UserName']     # 对手方id
                                # content = msg['Text']
                                
                            # self.chatsHistory[i]=lastMessage[2]
                        self.chatsHistory[session]=messages[-10:]

                    
            except Exception as e:
                print(e)
        if len(self.send_message_queue)>0:
            for i in self.send_message_queue:
                self.wx.ChatWith(i['session'])
                # self.wx.SendMsg(i['content'])
                messages=self.wx.GetAllMessage
                self.chatsHistory[i['session']]=messages[-10:]

            self.send_message_queue=[]

        self.timer = Timer(1,self.tick)
        self.timer.start()


def get_ui_by_childs(root,childs):
    node=root
    for i in childs:
        node=node.GetChildren()[i]
    return node
# def get_max_same(lista,listb,check):



default = Service
