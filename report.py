import json
import time
import requests
from datetime import datetime
import traceback

url = "https://access.nankai.edu.cn/Apply/Index/addApply?time=1695736206000"
server_chan_url = 'https://sc.ftqq.com/{}.send/'
server_chan_key = 'SCT224851TNiTzonroPkhzeBOddxUNwEzw'

# def post_and_print(s, url, data, headers, cookies):
#     result = s.post(url, data=json.dumps(data), headers=headers, cookies=cookies)
#     print(json.loads(result.text))
#     # print(
#     #     time.strftime("%m/%d %H:%M:%S ", time.localtime())
#     #     + " "
#     #     + json.loads(result.text)
#     # )

def server_chan_send(key, content, description):
    """
    使用server酱推送消息

    Args:
        key: API Key (SCKEY)
        content: 消息的标题
        description: 消息的具体内容

    Returns:
        str, http响应
    """
    get_url = server_chan_url.format(key)
    param = dict()
    param['text'] = content
    param['desp'] = description.replace('\n', '\n\n')  # 将格式改为MarkDown格式
    return requests.get(get_url, param)  # 使用requests自带的编码库来避免url编码问题

def message(server_chan_key, content, description):
    """
    向控制台打印消息，并会根据传入的用户信息判断是否使用server酱或者邮件推送

    Args:
        user: 用户信息
        content: 消息的标题
        description: 消息的具体内容
    """
    print(content)  # 控制台打印消息
    if len(description):
        print('\033[31m'+description+'\033[0m')

    if len(server_chan_key) > 0:
        server_chan_send(server_chan_key, content, description)  # 使用server酱发送

def report():
    """
    申请上报主逻辑,使用post直接向目标url post表单数据
    """
    # init
    s = requests.session()
    headers = {}

    # report
    cookies = {}
    data = {"q1-2": "20180169", "q1": "N", "q11": "刘健", "q2": "陈宋康", "q9": "居民身份证", "q3": "431025200207141615", "q10": "18570268868",
            "q4": "2023-09-27T07:30", "q5": "2023-09-27T22:30", "q6": "Y", "q13": "1", "q7": "", "q8": "N", "q12": "Y"}
    
    import datetime
    # 获取当天日期
    current_date = datetime.date.today()
    # 计算明天的日期
    tomorrow_date = (current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT")

    data["q4"]=tomorrow_date+"07:30"
    data["q5"]=tomorrow_date+"20:30"

    requestdata="data=" + json.dumps(data)
    print(requestdata)
    requestdata=requestdata.encode("utf-8")
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    
    print('客户端请求JSON报文数据为（客户端 --> 服务端）:\n',requestdata)
     
    #客户端发送请求报文到服务端
    result = requests.post(url,data=requestdata,headers=head)
    
    #客户端获取服务端的响应报文数据
    responsedata=json.loads(result.text)
    print('服务端的响应报文为（客户端 <--服务端）: ',responsedata)
    print("get the status: ",result.status_code)
    print("test-result:code+message:", responsedata['code'] + " "+ responsedata['message'])
    return result


if __name__ == "__main__":
    try:
        result = report()
        responsedata=json.loads(result.text)
        if result.status_code != '001':
            exception = traceback.format_exc()
            message(server_chan_key, responsedata['code'] + " "+ responsedata['message'] , exception)
    except Exception:
        exception = traceback.format_exc()
        message(server_chan_key,'每日上报程序运行出错，请尝试手动重新填报', exception)
