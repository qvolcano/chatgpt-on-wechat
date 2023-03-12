import requests

def default(args):
    print(2)
    return requests.get("http://v.api.aa1.cn/api/yiyan/index.php",verify=False).text