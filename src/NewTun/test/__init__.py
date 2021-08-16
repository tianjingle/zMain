import datetime

for i in range(10):
    print(i)

collectDate='2021-08-03 0:00:00'
collectDateSp = datetime.datetime.strptime(collectDate, '%Y-%m-%d %H:%M:%S')
endDate = '2021-08-06  0:00:00'
endDateSp = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
a=endDateSp-collectDateSp
print(a.days)