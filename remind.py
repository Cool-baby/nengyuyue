import sys
import time


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


notify(f"现在是 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 啦！\n"
       f"该去洗澡啦！\n"
       f"不洗澡的话别忘了取消！\n"
       f"\n"
       f"点击下面传送门直接传送至能预约\n"
       f"↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n"
       f"<a href='http://ligong.deshineng.com:8082/brmclg/html/main.html'>**/*能预约传送门*\\**</a>\n"
       f"↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑\n")


# 推送服务
pushplus_bot("10点啦！该去洗澡啦！", allMess)
