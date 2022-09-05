import random
import sys
import threading
import requests
import json
import time

# 读取account.py内的用户数据
try:
    from account import accounts

    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []

# 调用pushplus
try:
    from pushplus import pushplus_bot
except Exception as error:
    print(f'失败原因，推送配置有误:{error}')
    sys.exit(0)

# 配信内容格式
allMess = ''


def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'


# 日志录入时间
notify(f"能预约——浴室自动取消Beta\n"
       f"时间:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
       f"-----------/* _ *\\-----------\n")

# 定义URL，firsturl为URL的前半部分，firstvalue为时间段代码，根据我的测试，南区男浴室9.30-9.50代码为558，北区男浴室为478，前一个时间段代码-1
# global firstvalue
# firstvalue = 679
# 获取已经预约前缀
getBookOrderUrlFirst = 'http://ligong.deshineng.com:8082/brmclg/api/bathRoom/getBookOrderList?time='
# 取消预约前缀
cancelOrderUrlFirst = 'http://ligong.deshineng.com:8082/brmclg/api/bathRoom/cancelOrder?time='


# 预约方法
def yuyue(student):
    nowtime = round(time.time() * 1000)
    getBookOrderUrl = getBookOrderUrlFirst + str(nowtime) + '&_=' + str(1662340065841)
    headers = {
        'Host': 'ligong.deshineng.com:8082',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,eu;q=0.8,ja;q=0.7,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'token': student['token'],
        'loginid': student['loginid'],
        'User - Agent': student['UA'],
    }
    # 将response转为json格式
    responseGetBook = requests.get(url=getBookOrderUrl, headers=headers).json()

    status_code = responseGetBook['code']
    if status_code == 200:
        notify(f"{student['user']}\t登录成功")
        if responseGetBook['data']['bookOrderList']:
            bookOrderId = responseGetBook['data']['bookOrderList'][0]['id']
            nowtime2 = round(time.time() * 1000)
            # 取消预约URL
            cancelOrderUrl = cancelOrderUrlFirst + str(nowtime2) + '&bookorderid=' + str(bookOrderId)
            responseCancel = requests.post(url=cancelOrderUrl, headers=headers).json()
            if responseCancel['code'] == 200:
                notify(f"{student['user']}\t成功取消预约 \n"
                       f"取消预约详细信息：\n"
                       f"学号：{responseGetBook['data']['bookOrderList'][0]['studentName']}\n"
                       f"取消时间段：{responseGetBook['data']['bookOrderList'][0]['period']}")
            else:
                notify(f"{student['user']}\t取消预约失败")
        else:
            notify(f"{student['user']}\t没有预约")
    else:
        # print("{0}登录失败".format(student['user']))
        notify(f"{student['user']}\t登录失败")
        return False


# 主函数
if __name__ == '__main__':

    try:
        for user in lists:
            # firstvalue = user['timeId']
            threading.Thread(target=yuyue, args=(user,)).start()

    except Exception as error:
        # print(f'失败原因:{error}')
        notify(f'失败原因:{error}')

    time.sleep(2)
    # 推送服务
    pushplus_bot("浴室取消预约Beta", allMess)
