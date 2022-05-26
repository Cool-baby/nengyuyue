'''
本文件为账户配置文件
其中accounts是登录能预约抓的token、UA、loginid。user为备注，可为任意值。timeId为用户自定义的时间段。
若有多个用户，可在accounts里面直接加，主函数可以使用多线程直接运行。（因为服务器单核，所以多线程）
其中push_config是pushplus推送加的配置，PUSH_PLUS_TOKEN是token。PUSH_PLUS_USER一对多推送用得到，一对一推送此值可为空。
pushplus详情见https://www.pushplus.plus/
'''


accounts = [
    {
        'user': '',
        'token': '',
        'UA': '',
        'loginid': ''
        'timeId': ''
    },
    {
        'user':'',
        'token':'',
        'UA':'',
        'loginid':''
        'timeId': ''
    }
]
push_config = [
    {
        'PUSH_PLUS_TOKEN': '',                                              # push+ 微信推送的用户令牌
        'PUSH_PLUS_USER': '',                                               # push+ 微信推送的群组编码
    }
]
