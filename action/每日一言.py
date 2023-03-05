import requests
def main(args,context):
    return requests.get("http://v.api.aa1.cn/api/yiyan/index.php",verify=False).text