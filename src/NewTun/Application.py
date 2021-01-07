import math

import pandas as pd
import talib

from src.NewTun.ChipCalculate import ChipCalculate
from src.NewTun.DrawPicture import DrawPicture
from src.NewTun.LeastSquare import LeastSquare
from src.NewTun.LoopBack import LoopBack
from src.NewTun.QueryStock import QueryStock
import numpy as np

class Application:


    window=160
    downlimit=-20
    indexCloseDict={}
    least = LeastSquare()
    loopBack=LoopBack()
    queryStock=QueryStock()
    avgCostGrad=0
    cvValue=-1
    maxPrice=0
    currentPrice=0
    isDownLine=0

    def setStackCode(self):
        least=LeastSquare()
        draw = DrawPicture()
        loopBack = LoopBack()
        queryStock = QueryStock()
        queryStock.init(self.window)
        self.indexCloseDict={}
        return


    #筹码计算
    def chipCalculate(self,result, start,isProd):
        chipCalculateList = []
        for index, row in result.iterrows():
            temp = []
            currentIndex = index - start
            temp.append(currentIndex)
            temp.append(row['open'])
            temp.append(row['high'])
            temp.append(row['low'])
            temp.append(row['close'])
            temp.append(row['volume'])
            temp.append(row['tprice'])
            temp.append(row['turn'])
            temp.append(int(row['tradestatus']))
            chipCalculateList.append(temp)
        if isProd==False:
            chipCalculateList=chipCalculateList[-112:]
        calcualate = ChipCalculate()
        resultEnd = calcualate.getDataByShowLine(chipCalculateList)
        del calcualate
        return resultEnd

    def cv(self,temp):
        # print(temp)
        # minTemp=temp[0][1]
        # for i in range(len(temp)):
        #     if temp[i][1]!=0 and temp[i][1]<minTemp:
        #         minTemp=temp[i][1]
        # print(minTemp)
        # temp[:,1]=temp[:,1]-minTemp
        sumF=np.sum(temp[:,1])
        sumfx=0
        sumfdoubleX=0
        for i in range(len(temp)):
            #次数
            f=temp[i][1]
            price=(temp[i][0] / 100)
            sumfx=sumfx+f*price
            sumfdoubleX=sumfdoubleX+f*price*price
        sumfx=sumfx*sumfx
        rightup=sumfx/sumF
        result=math.sqrt((sumfdoubleX-rightup)/sumF)
        print("--方差"+str(result))
        return result

    #执行器
    def execute(self,code):
        result=self.queryStock.queryStock(code)
        if len(result[0])<200:
            return self
        return self.core(result[0],result[1])


    #核心调度器
    def core(self,result,maxPrice):
        self.maxPrice=maxPrice
        #十四天
        Kflag=self.least.everyErChengPrice(result,14,False)
        #三十天
        erjieSlow = self.least.everyErChengPrice(result, 30,False)
        # 三天二阶导数
        erjieK=self.least.doubleErJie(Kflag, 3,False)
        #慢速一阶导数
        wangXSlow = []
        wangYSlow = []
        for item in erjieSlow:
            kX1 = item[0]
            kk1 = item[1]
            wangXSlow.append(kX1)
            wangYSlow.append(kk1)
        yijieSlowdict = dict(zip(wangXSlow, wangYSlow))
        # 筹码计算
        resultEnd = self.chipCalculate(result, self.queryStock.start,False)
        choumaList=np.array(resultEnd[2][2])
        x = []
        p = []
        resultEnd.sort(key=lambda resultEnd: resultEnd[0])
        for i in range(len(resultEnd)):
            x.append(resultEnd[i][0])
            p.append(resultEnd[i][1])
        myResult = pd.DataFrame()
        myResult['tprice'] = p
        tianjingle = self.least.everyErChengPriceForArray(np.array(x), np.array(p), 30)
        x1 = []
        y1 = []
        if tianjingle==None:
            return
        for item in tianjingle:
            kX = item[0]
            kk = item[1]
            x1.append(kX)
            y1.append(kk)
        pingjunchengbendic = dict(zip(x1, y1))
        total=len(result)
        for i in range(len(erjieK)):
            item = erjieK[i]
            currentx = item[0]
            onkslow = yijieSlowdict.get(currentx)
            onkchengben = pingjunchengbendic.get(currentx)
            if onkslow == None or onkchengben == None:
                continue
            if onkslow < 0 and onkchengben < 0:
                onslowyestaday = yijieSlowdict.get(currentx - 1)
                chengbenyestaday = pingjunchengbendic.get(currentx - 1)
                if onslowyestaday == None or chengbenyestaday == None:
                    continue
                if onslowyestaday < 0 and chengbenyestaday < 0 and onslowyestaday < onkslow and onkchengben < chengbenyestaday:
                    if currentx==total-1:
                        self.avgCostGrad=onkchengben
                        self.cvValue = self.cv(choumaList)
                        self.currentPrice=float(result['close'][len(result)-1])
                        if self.currentPrice<=self.maxPrice*0.618:
                            self.isDownLine=1
                        else:
                            self.isDownLine=0
                        print(self.currentPrice)
                        print(self.maxPrice)
                        print(self.isDownLine)

        self.least=None
        self.loopBack=None
        self.queryStock=None
        return self





