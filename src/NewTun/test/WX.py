import json
from threading import Timer
from wxpy import *
import requests
import urllib.parse

def get_news():
    '''获取金山词霸每日一句'''
    url = 'http://open.iciba.com/dsapi'
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note

def send_news():
    val = 1
    bot = Bot()  # 连接微信,会出现一个登陆微信的二维码
    try:
        # my_friends =bot.friends().search(u'XXX')[0]#这里是你微信好友的昵称
        friends = bot.friends()
        for i in friends:
            name = i
            print(name.name)
            if "Lele" == name.name:
                name.send(u'今天消息发送失败了')
            else:
                print(name)
                break
        # my_friend.send(contents[0])
        # my_friend.send(contents[1])
        # name.send(mssage)
        # t = Timer(86400, send_news)  # 这里是一天发送一次，86400s = 24h
        # t.start()
    except:
        print(1)
        # my_friend = bot.friends().search('filehelper')[0]
        # my_friend.send(u'今天消息发送失败了')

def getRequest():
    _header = getHeader()
    _data = urllib.parse.urlencode(getData()).encode('utf-8')
    url = 'https://webapi.huilv.cc/api/trend/yaho'
    response = requests.post(url, data=_data, headers=_header)

    print(response.encoding)
    print(response.apparent_encoding)
    r = response.text
    result_text = json.loads(r, encoding='utf-8')
    val = result_text["obj"][len(result_text["obj"]) -1 ]["huilv"]
    return val

def getHeader():
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.huilv.cc/zoushitu?a=JPYCNY&time=d1',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    return header

def getData():
    paydata = {
        'pinzhong': 'JPYCNY',
        'longs': 'd1'
    }
    return paydata

if __name__ == '__main__':
    get_news()
    send_news()