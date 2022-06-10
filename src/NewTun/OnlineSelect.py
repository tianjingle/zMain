import os
import time

import pendulum

from src.NewTun.QueryStock import QueryStock
from src.NewTun.RunTimeExecute import RunTimeExecute


class OnlineSelect:

    onlineDir=os.path.dirname(__file__)+"/online/"
    time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    onlinePath=os.path.dirname(__file__)+"/online/"+time+"-cache.txt"

    def __init__(self):
        if os.path.exists(self.onlineDir)==False:
            os.mkdir(self.onlineDir)

    def doParseType(self,type):
        if type == 99:
            return "反转反弹"
        if type == 7:
            return "超级"
        if type == 6:
            return "纯动力"
        if type == 5:
            return "旺角动力"
        if type ==4:
            return "反弹"
        if type==3:
            return "好望角"
        if type ==2:
            return "分水岭"
        if type ==1:
            return "高位反弹"
        return ""

    def selectStockByDb(self):
        #开始运行的时间
        list = []
        endTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        query=QueryStock()
        #查到所有的股票
        codes=query.queryStockToday(endTime)
        for item in codes:
            type=self.doParseType(item[2])
            result=item[0]+"\t"+item[1]+"\t"+type
            list.append(result)
        return list

    def read2Memory(self):
        list=[]
        fo = open(self.onlinePath,"r",encoding='gbk')
        for line in fo.readlines():
            if line!='\n':
                list.append(line.replace("\n",""))
        fo.flush()
        fo.close()
        return list

    #每次启动的时候都清空一下
    def clearOnlineTxt(self):
        list=[]
        f = open(self.onlinePath, "w", encoding='gbk')
        f.writelines(list)
        f.flush()
        f.close()

    def write2OnlineTxt(self):
        endTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        markRunTimeHour=RunTimeExecute().fetchMarkRunTimeHour()
        t = pendulum.parse(endTime).day_of_week
        #周内并且盘中
        if markRunTimeHour<15 and markRunTimeHour>=9 and t>=1 and t<=5:
            #old
            oldList=self.read2Memory()
            #new
            list=self.selectStockByDb()
            #current
            list=oldList+list
            result=[]
            for item in list:
                result.append(item+"\n")
            f = open(self.onlinePath, "w", encoding='gbk')
            f.writelines(result)
            f.flush()
            f.close()
            QueryStock().deleteStockByTime(endTime)

# OnlineSelect().write2OnlineTxt()