import requests
def main(args,context):
    return requests.get("https://api.oick.cn/dutang/api.php",verify=False).text
