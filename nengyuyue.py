import requests
import json

try:
    from account import accounts
    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []

global firstvalue
firstvalue = 558
firsturl = 'http://ligong.deshineng.com:8082/brmclg/api/bathRoom/bookOrder?time=1637818278759&bookstatusid='


def login(aurl,avalue):
    url = aurl+str(avalue)
    headers = {
        'Host': 'ligong.deshineng.com:8082',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,eu;q=0.8,ja;q=0.7,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'token': lists[0]['token'],
        'loginid': lists[0]['loginid'],
        'User - Agent': lists[0]['UA'],
    }
    response = requests.post(url=url, headers=headers).json()
    #print(response)
    status_code = response['code']
    succeedflag = response['data']['succeed']
    #print(status_code)
    #print(succeedflag)
    if status_code == 200:
        print("{0}登录成功".format(lists[0]['user']))
        if succeedflag == 'Y':
            print("{0}预约成功".format(lists[0]['user']))
            print("预约信息：ID：{0}，浴室：{1}，时间：{2}，学号：{3}，创建时间：{4}".format(response["data"]["bookOrderList"][0]['id'],
                                                                     response["data"]["bookOrderList"][0]['bathRoomName'],
                                                                     response["data"]["bookOrderList"][0]['period'],
                                                                     response["data"]["bookOrderList"][0]['studentName'],
                                                                     response["data"]["bookOrderList"][0]['createTimeStr']))
        else:
            print("{0}预约失败".format(lists[0]['user']))
            global firstvalue
            print("代号：{0} 时间段预约失败！succeedflag = {1}，正在尝试预约上一个时间段！".format(firstvalue,succeedflag))
            firstvalue-=1
            login(firsturl,firstvalue)
    else:
        print("{0}登录失败".format(lists[0]['user']))
        return False


if __name__ == '__main__':
    try:
        login(firsturl,firstvalue)
    except Exception as error:
        print(f'失败原因:{error}')