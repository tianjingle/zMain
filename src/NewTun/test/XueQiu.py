#-*- coding: utf-8 -*-
import requests
import urllib.request
import json
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib.dates import AutoDateLocator, DateFormatter ,DayLocator
from matplotlib.ticker import AutoLocator
import re
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
#设置matplotlib中文字体
font = FontProperties(fname=r"c:\\windows\\fonts\\simsun.ttc", size=14)
#伪装浏览器登录
headers={
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}
#可以写一个url管理器来对url列表进行操作，此处先行指定几个
url=["https://xueqiu.com/S/NVDA","https://xueqiu.com/S/AMD","https://xueqiu.com/S/TSLA","https://xueqiu.com/S/BABA","https://xueqiu.com/S/AAPL"]
#抓取现在股票价格
def get_price(url):
	response=urllib.request.Request(url,headers=headers)
	html=urllib.request.urlopen(response).read().decode("utf-8")
	soup=BeautifulSoup(html,"html.parser")
	name=soup.find("div",class_="stock-name").get_text()
	price=soup.find("div",class_="stock-current").get_text()
	print(name+"现在的股价是:"+price)
for u in url:
	get_price(u)
#抓取Tesla股票历史价格
history_url="https://finance.yahoo.com/quote/TSLA/history?ltr=1"
Date=[]
Open=[]
High=[]
Low=[]
Close=[]
def get_history_price(url,headers):
	response=urllib.request.Request(url,headers=headers)
	html=urllib.request.urlopen(response).read().decode("utf-8")
	soup=BeautifulSoup(html,"html.parser")
#查找日期,根据data-reactid属性寻找标签
	x=52
	while x<=1537:
		date=soup.find("td",attrs={"data-reactid":x}).get_text()
		Date.append(date)
		x=x+15
#查找开盘价格
	x=54
	while x<=1539:
		op=soup.find("td",attrs={"data-reactid":x}).get_text()
		Open.append(op)
		x=x+15
#查找高位价格
	x=56
	while x<=1541:
		high=soup.find("td",attrs={"data-reactid":x}).get_text()
		High.append(high)
		x=x+15
#查找低位价格
	x=58
	while x<=1543:
		low=soup.find("td",attrs={"data-reactid":x}).get_text()
		Low.append(low)
		x=x+15
#查找收盘价格
	x=60
	while x<=1545:
		close=soup.find("td",attrs={"data-reactid":x}).get_text()
		Close.append(close)
		x=x+15
	test=soup.find("td",attrs={"data-reactid":54})
get_history_price(history_url,headers)
print("绘图中")
#将Date转化为matplotlib可识别的格式
Date.reverse()
Date_new=[]
for d in Date:
	d=d.replace("Dec ","12/")
	d=d.replace("Nov ","11/")
	d=d.replace("Oct ","10/")
	d=d.replace("Sep ","09/")
	d=d.replace("Aug ","08/")
	d=d.replace("Jul ","07/")
	d=d.replace("Jun ","06/")
	d=d.replace("May ","05/")
	d=d.replace("Apr ","04/")
	d=d.replace("Mar ","03/")
	d=d.replace("Feb ","02/")
	d=d.replace("Jan ","01/")
	d=d.replace(", ","/")
	Date_new.append(d)
Date_new=[datetime.strptime(d, '%m/%d/%Y').date() for d in Date_new]
Date=Date_new
Open.reverse()
Close.reverse()
def print_mat():
	fig1=plt.figure()
	ax1=fig1.add_subplot(1,1,1)
	ax1.xaxis.set_major_formatter(DateFormatter('%m-%d'))#设置时间标签显示格式
	ax1.xaxis.set_major_locator(AutoDateLocator())#设置x轴自动时间刻度
	ax1.yaxis.set_major_locator(AutoLocator())#设置y轴自动刻度
	plt.plot(Date,Open,label="Open",color="red")
	plt.plot(Date,Close,label="Close",color="blue")
	plt.title(u"抓取特斯拉股票历史开盘、收盘价格",fontproperties=font)
	plt.xlabel("时间",fontproperties=font)
	plt.legend()
	plt.show()
print_mat()
#抓取价值@风险持仓变化情况
# hold_headers={
# 	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
# }
# hold_url="https://xueqiu.com/P/ZH011943"
# def get_hold_change(url):
# 	# response=urllib.request.Request(hold_url,headers=headers)
# 	# html=urllib.request.urlopen(response).read().decode("utf-8")
# 	# data = re.findall('SNB.cubePieData',html)
# 	# print(data)
# 	# print(data['list'][0]['rebalancing_histories'][0]['stock_name'],end='   持仓变化')
# 	res=requests.get(url)
# 	# data=res.status_code()
# 	# print(data)
# get_hold_change(hold_url)
# for each in url:
# 	get_price(each,headers)
