from manager import ServiceManager
def main():
    service=ServiceManager.get("WechatService")
    service.login()
    

default = main