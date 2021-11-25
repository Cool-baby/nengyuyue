import json
import requests


try:
    from account import push_config
    lists = push_config
except Exception as error:
    print(f'失败原因:{error}')
    lists = []


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    print("PUSHPLUS 服务启动")

    url = "http://www.pushplus.plus/send"
    data = {
        "token": lists[0]["PUSH_PLUS_TOKEN"],
        "title": title,
        "content": content,
        "topic": lists[0]["PUSH_PLUS_USER"],
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url=url, data=body, headers=headers, timeout=15)
        try:
            datas = response.json()
            if datas.get("code") == 200:
                print("PUSHPLUS 推送成功！")
            elif datas.get("code") == 600:
                url2 = "http://pushplus.hxtrip.com/send"
                response2 = requests.post(
                    url=url2, data=body, headers=headers, timeout=15
                )
                try:
                    datas2 = response2.json()
                    if datas2.get("code") == 200:
                        print("PUSHPLUS(hxtrip) 推送成功！")
                    elif datas2.get("code") == 600:
                        print("PUSHPLUS 推送失败！PUSH_PLUS_TOKEN 错误。")
                    else:
                        print(f"PUSHPLUS(hxtrip) 推送失败！响应数据：{datas2}")
                except json.JSONDecodeError:
                    print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response2.text}")
            else:
                print(f"PUSHPLUS 推送失败！响应数据：{datas}")
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息：\n{traceback.format_exc()}")