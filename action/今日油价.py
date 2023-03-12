import requests
import json
def default(args):
    res=requests.get("https://www.mxnzp.com/api/oil/search?province=广东&app_id=rgihdrm0kslojqvm&app_secret=WnhrK251TWlUUThqaVFWbG5OeGQwdz09",verify=False)
    data=json.loads(res.text)
    out=""
    for i in data['data']:
        if i=="province":
            out+=data['data'][i]+"\n"
        else:
            out+=i+":"+data["data"][i]+"\n"
    return out