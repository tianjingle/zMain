import datetime

import requests

import akshare as ak

import pendulum

t=pendulum.parse("2022-05-23").day_of_week
print(t)

add_hour = datetime.datetime.now()
now_hour = add_hour.strftime('%H')
print(now_hour)
if int(now_hour) < 17:
    print(now_hour)