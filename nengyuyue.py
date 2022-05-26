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
notify(f"能预约——浴室自动预约\n"
       f"时间:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
       f"--------/* _ *\\--------\n")


# 定义URL，firsturl为URL的前半部分，firstvalue为时间段代码，根据我的测试，南区男浴室9.30-9.50代码为558，北区男浴室为478，前一个时间段代码-1
global firstvalue
# firstvalue = 679
firsturl = 'http://ligong.deshineng.com:8082/brmclg/api/bathRoom/bookOrder?time='


# 预约方法
def yuyue(student, firstUrl, value):
    avalue = value
    firstime = round(time.time() * 1000)
    url = firstUrl + str(firstime) + '&bookstatusid=' + str(avalue)
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
    response = requests.post(url=url, headers=headers).json()
    # print(response)
    status_code = response['code']
    succeedflag = response['data']['succeed']
    # print(status_code)
    # print(succeedflag)
    if status_code == 200:
        # print("{0}登录成功".format(student['user']))
        notify(f"{student['user']}\t登录成功")
        if succeedflag == 'Y':
            # print("{0}预约成功".format(student['user']))
            notify(f"{student['user']}\t预约成功")
            '''
            print("预约信息：ID：{0}，浴室：{1}，时间：{2}，学号：{3}，创建时间：{4}".format(response["data"]["bookOrderList"][0]['id'],
                                                                     response["data"]["bookOrderList"][0]['bathRoomName'],
                                                                     response["data"]["bookOrderList"][0]['period'],
                                                                     response["data"]["bookOrderList"][0]['studentName'],
                                                                     response["data"]["bookOrderList"][0]['createTimeStr']))
            '''
            notify(f"预约信息：\n"
                   f"ID：{response['data']['bookOrderList'][0]['id']}\n"
                   f"学号：{response['data']['bookOrderList'][0]['studentName']}\n"
                   f"浴室：{response['data']['bookOrderList'][0]['bathRoomName']}\n"
                   f"预约时间：{response['data']['bookOrderList'][0]['period']}\n"
                   f"创建时间：{response['data']['bookOrderList'][0]['createTimeStr']}\n")
        else:
            # print("{0}预约失败".format(student['user']))
            notify(f"{student['user']}\t预约失败")
            # print("代号：{0} 时间段预约失败！succeedflag = {1}，正在尝试预约上一个时间段！".format(firstvalue,succeedflag))
            notify(f"代号：{avalue} 时间段预约失败！\n"
                   f"succeedflag = {succeedflag}\n"
                   f"正在尝试预约上一个时间段！\n"
                   f"--------------------\n")
            avalue -= 1
            # yuyue(firsturl,firstvalue)
            if avalue < 558:
                notify(f"不预约时间太早的！\n 结束预约 \n")
                return False
            else:
                yuyue(student, firsturl, avalue)
    else:
        # print("{0}登录失败".format(student['user']))
        notify(f"{student['user']}\t登录失败")
        return False


# 主函数
if __name__ == '__main__':
    start = time.time()
    try:
        for user in lists:
            firstvalue = user['timeId']
            threading.Thread(target=yuyue, args=(user, firsturl, firstvalue)).start()

    except Exception as error:
        # print(f'失败原因:{error}')
        notify(f'失败原因:{error}')

    end = time.time()
    notify(f"本次预约用时：{end-start} 秒\n")
    time.sleep(2)
    # 推送服务
    pushplus_bot("浴室预约", allMess)
