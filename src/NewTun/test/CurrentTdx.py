import requests
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题


def get_html(url):
    try:
        response = requests.get(url=url)
        print(response)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.json()
    except:
        print('Error_get_html')
        return ''


def get_data(infos):
    data = []
    for info in infos:
        columns = info.keys()
        data.append(info.values())
    data = pd.DataFrame(data=data, columns=columns)
    return data






class Df:
    def __init__(self, data):
        data['day'] = pd.to_datetime(data['day'])
        data = data.set_index('day')
        self.data = data.astype(float)

    def visual(self):
        style = ['-.', '--', '-', ':']
        self.data[['open', 'high', 'low', 'close']].plot(title='股票价格波动趋势图',ylabel='prices', style=style)
        plt.show()
        self.data[['volume']].plot(title='股票成交量波动趋势图', ylabel='numbers')
        plt.show()


def main():
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/' \
          'CN_MarketData.getKLineData?symbol=sz000009&scale=60&ma=no&datalen=2'
    # infos = get_html(url)  # 获取数据

    # url="https://xueqiu.com/S/SZ000009"
    response = requests.get(url=url)
    print(response)
    print(response.text)


    # print(infos)
    # data = get_data(infos)  # 处理数据
    # print(data)





if __name__ == "__main__":
    main()