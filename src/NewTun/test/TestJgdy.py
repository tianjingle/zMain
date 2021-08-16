import datetime
import time

from src.NewTun.Application import Application
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
        sql = "select * from candidate_stock where collect_date>'"+startTimeStock+"'"
        stocks=query.queryStockForTestJgdy(sql)
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

    def testXiChouZS(self):
        resultSuccess=[]
        resultFail=[]
        query=QueryStock()
        sql = "select * from candidate_stock where zsm=2 and profit!=0"
        stocks=query.queryStockForTestJgdy(sql)
        for item in stocks:
            collectDate = item[2]+' 0:00:00'
            collectDateSp = datetime.datetime.strptime(collectDate, '%Y-%m-%d %H:%M:%S')
            endDate = item[8]+' 0:00:00'
            endDateSp = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
            a = endDateSp - collectDateSp
            testBefore=a.days
            queryStock = QueryStock()
            result=queryStock.queryStock(item[0])
            result=result[0]
            z = float(result['z'][len(result) - int(testBefore)])
            s = float(result['s'][len(result) - int(testBefore)])
            m = float(result['m'][len(result) - int(testBefore)])
            if float(item[7])>0 and z>s:
                resultSuccess.append(item)
            if float(item[7]<0) and z>s:
                resultFail.append(item)

        for t in resultSuccess:
            print(t)
        print("--------")
        for t in resultFail:
            print(t)

        print("成功："+str(len(resultSuccess)))
        print("失败："+str(len(resultFail)))
        print("总计："+str(len(stocks)))



    def testXiChouSanJx(self):
        resultSuccess=[]
        resultFail=[]
        query=QueryStock()
        sql = "select * from candidate_stock where zsm=1 and profit!=0"
        stocks=query.queryStockForTestJgdy(sql)
        for item in stocks:
            collectDate = item[2]+' 0:00:00'
            collectDateSp = datetime.datetime.strptime(collectDate, '%Y-%m-%d %H:%M:%S')
            endDate = item[8]+' 0:00:00'
            endDateSp = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
            a = endDateSp - collectDateSp
            testBefore=self.workdays(item[2],item[8])
            print(testBefore)
            queryStock = QueryStock()
            result=queryStock.queryStock(item[0])
            result=result[0]
            application=Application()
            resultEnd=application.chipCalculate(result,0,False)
            resultEnd.sort(key=lambda resultEnd: resultEnd[0])
            sanJx = resultEnd[len(resultEnd) - testBefore][7]

            if float(item[7])>0 and sanJx>0:
                print("2")
                print(item[2])
                resultSuccess.append(item)
            if float(item[7]<0) and sanJx>0:
                print("1")
                print(item[2])
                resultFail.append(item)

        for t in resultSuccess:
            print(t)
        print("--------")
        for t in resultFail:
            print(t)

        print("成功："+str(len(resultSuccess)))
        print("失败："+str(len(resultFail)))
        print("总计："+str(len(stocks)))

    def workdays(self,start,end):
        '''
        计算两个日期间的工作日
        start:开始时间
        end:结束时间
        '''
        from datetime import datetime,timedelta
        from chinese_calendar import is_workday
         # 字符串格式日期的处理
        if type(start) == str:
            start = datetime.strptime(start,'%Y-%m-%d').date()
        if type(end) == str:
            end = datetime.strptime(end,'%Y-%m-%d').date()
        # 开始日期大，颠倒开始日期和结束日期
        if start > end:
            start,end = end,start
        counts = 0
        while True:
            if start > end:
                break
            if is_workday(start):
                counts += 1
            start += timedelta(days=1)
        return counts
