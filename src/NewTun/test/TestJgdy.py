import datetime
import time

from src.NewTun.JgdyQuery import JgdyQuery
from src.NewTun.QueryStock import QueryStock

class TestJgdy:

    def test(self):
        str_p = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
        startTimeStock = (dateTime_p + datetime.timedelta(days=-100)).strftime("%Y-%m-%d")
        startTimeJG = (dateTime_p + datetime.timedelta(days=-150)).strftime("%Y-%m-%d")
        query=QueryStock()
        jgdy=JgdyQuery()
        stocks=query.queryStockForTestJgdy(startTimeStock)
        print(len(stocks))
        jgdy=jgdy.queryAllByDate(startTimeJG)
        upCount=0
        downCount=0
        result=[]
        resultFail=[]
        for item in stocks:
            wang=item[0].split('.')[1]
            for z in jgdy:
                endTime=item[2]+" 0:29:08"
                dateTime_p = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
                startTimeStock = (dateTime_p + datetime.timedelta(days=-60)).strftime("%Y-%m-%d")
                if item[7]!=None and z[0]== wang and z[2]>startTimeStock and z[2]<item[2] and float(item[7])>0 :
                    upCount=upCount+1
                    result.append(item)
                    break
                elif item[2]!=None and item[7]!=None and z[0]== wang and z[2]>startTimeStock and z[2]<item[2] and float(item[7])<0:
                    downCount=downCount+1
                    resultFail.append(item)
                    break
                else:
                    continue
        print(upCount)
        print(downCount)
        result=sorted(result,key=lambda x:x[7],reverse=True)
        for t in result:
            print(t)
        print("----------------------------")
        resultFail=sorted(resultFail,key=lambda x:x[7])
        for t in resultFail:
            print(t)
        if downCount<=0:
            print("机构调研股全部涨了~~~")
            return
        print(upCount/downCount)

