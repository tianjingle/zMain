import datetime
import json
import os
import time



class RunTimeExecute:

    RunTimeCacheMap={}

    #运行的时间
    RunTime=None

    #开始运行的时间
    runTimePath = os.path.join(os.path.dirname(__file__), "RunTime")


    #运行的实时股票信息：时间_code_info
    runTimeCachePath = os.path.join(os.path.dirname(__file__), "RunTimeCache")

    #打一个桩
    def markRunTime(self):
        #运行的小时数字
        RunTime=time.localtime().tm_hour
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        mark=today+"_"+str(RunTime)
        f = open(self.runTimePath, "w", encoding='gbk')
        f.writelines(mark)
        f.flush()
        f.close()
        #每次运行的时候把上次缓存清理一下
        # self.clearRunTimeCache()

    #读取这个桩的值
    def fetchMarkRunTime(self):
        fo = open(self.runTimePath, "r", encoding='gbk')
        stockInfo=None
        for line in fo.readlines():
            infs = line.replace("\n", "")
            stockInfo = infs.split("_")
        if stockInfo!=None:
            #返回y-m-d,h
            return stockInfo[0],stockInfo[1]
        return None,None

    def fetchMarkRunTimeHour(self):
        fo = open(self.runTimePath, "r", encoding='gbk')
        stockInfo=None
        for line in fo.readlines():
            infs = line.replace("\n", "")
            stockInfo = infs.split("_")
        if stockInfo!=None:
            #返回y-m-d,h
            return int(stockInfo[1])
        return 16




    #将运行的股票实时信息转化为map
    def readRunTime2Map(self,date):
        fo = open(self.runTimeCachePath,"r",encoding='gbk')
        for line in fo.readlines():
            infs=line.replace("\n","")
            stockInfo=infs.split("_")
            if date==stockInfo[0]:
                self.RunTimeCacheMap[stockInfo[0]+"_"+stockInfo[1]]=stockInfo[2]
        fo.flush()
        fo.close()

    #将实时股票数据写入到文件
    def writeRunTime2Cache(self,stockInfos):
        f = open(self.runTimeCachePath, "a+", encoding='gbk')
        f.writelines(stockInfos+"\n")
        f.flush()
        f.close()

    def clearRunTimeCache(self):
        f = open(self.runTimeCachePath, "w", encoding='gbk')
        f.writelines("")
        f.flush()
        f.close()


# now = Tencent().getCurrentStockInfo("sz.000666")
# print(time.localtime().tm_hour)
# tian = {'date': "2022-06-06",
#          'code': "sz.000895",
#          'open': now['open'],
#          'high': now['high'],
#          'low': now['low'],
#          'close': now['now'],
#          'volume': now['volume'],
#          'tradestatus': 1,
#          'turn': now['turnover'],
#          'isST': 0}
# print(type(tian))
# RunTimeExecute().markRunTime()
# RunTimeExecute().writeRunTime2Cache("2022-06-06_sz.000666_"+str(json.dumps(tian)))
# RunTimeExecute().writeRunTime2Cache(str(tian))
# RunTimeExecute().clearRunTimeCache()