import pandas as pd

from src.NewTun.ChipCalculate import ChipCalculate
from src.NewTun.DrawPictureReal import DrawPictureReal
from src.NewTun.LeastSquare import LeastSquare
from src.NewTun.LoopBack import LoopBack
from src.NewTun.QueryStock import QueryStock
import numpy as np


class ApplicationWithDraw:
    window = 160
    downlimit = -20
    indexCloseDict = {}
    least = LeastSquare()
    draw = DrawPictureReal()
    loopBack = LoopBack()
    queryStock = QueryStock()
    avgCostGrad = 0

    def setStackCode(self):
        least = LeastSquare()
        draw = DrawPictureReal()
        loopBack = LoopBack()
        queryStock = QueryStock()
        queryStock.init(self.window)
        self.indexCloseDict = {}

    # 筹码计算
    def chipCalculate(self, result, start):
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
        calcualate = ChipCalculate()
        resultEnd = calcualate.getDataByShowLine(chipCalculateList,True)
        return resultEnd

    def executeForTest(self, code, savePath):
        result = self.queryStock.queryStock(code)
        if len(result[0]) < 200:
            return self
        return self.core(result[0], code, True, savePath, True)

    # 执行器
    def execute(self, code, isShow, savePath):
        result = self.queryStock.queryStock(code)
        if len(result[0]) < 200:
            return self
        return self.core(result[0], code, isShow, savePath, False)

    # 核心调度器
    def core(self, result, code, isShow, savePath, isTest):
        self.draw.showK(code, result, isShow, savePath)
        self.draw.isTest = isTest
        # 十四天
        Kflag = self.least.everyErChengPrice(result, 14, True)
        # 三十天
        erjieSlow = self.least.everyErChengPrice(result, 30, True)
        # 三天二阶导数
        erjieK = self.least.doubleErJie(Kflag, 3, True)
        # 将收盘价转化为字典
        testX = []
        testY = []

        H1 = []
        H2 = []
        H3 = []
        for index, row in result.iterrows():
            currentIndex = index - self.queryStock.start
            price = row['close']
            testX.append(currentIndex)
            testY.append(price)

            tempH1 = row['h1']
            tempH2 = row['h2']
            tempH3 = row['h3']

            if tempH1 == None:
                H1.append(0)
            else:
                H1.append(float(tempH1))
            if tempH2 == None:
                H2.append(0)
            else:
                H2.append(float(tempH2))
            if tempH3 == None:
                H3.append(0)
            else:
                H3.append(float(tempH3))

        self.indexCloseDict = dict(zip(testX, testY))

        self.draw.shenxianQS(testX, H1, H2, H3)

        # 一阶导数
        wangX = []
        wangY = []
        for item in Kflag:
            kX = item[0]
            kk = item[1]
            wangX.append(kX)
            wangY.append(kk)
        self.draw.ax1Show(wangX, wangY)
        yijiedict = dict(zip(wangX, wangY))

        # 二阶导数
        wangX = []
        wangY = []
        for item in erjieK:
            kX = item[0]
            kk = item[1]
            wangX.append(kX)
            wangY.append(kk)
        self.draw.ax2Show(wangX, wangY)

        # 慢速一阶导数
        wangXSlow = []
        wangYSlow = []
        for item in erjieSlow:
            kX1 = item[0]
            kk1 = item[1]
            wangXSlow.append(kX1)
            wangYSlow.append(kk1)
        self.draw.ax3showSlow(wangXSlow, wangYSlow)
        yijieSlowdict = dict(zip(wangXSlow, wangYSlow))

        # 筹码计算
        resultEnd = self.chipCalculate(result, self.queryStock.start)
        resultEnd.sort(key=lambda resultEnd: resultEnd[0])
        resultEndLength = len(resultEnd)
        string = ""
        x = []
        p = []
        priceBigvolPriceIndexs = []
        bigVolPrice = {}
        myUp = {}
        for i in range(len(resultEnd)):
            x.append(resultEnd[i][0])
            string = string + "," + str(resultEnd[i][1])
            p.append(resultEnd[i][1])
            if i == resultEndLength - 1:
                priceJJJ = resultEnd[i][1]
            # 价格大于50%的筹码线
            if resultEnd[i][5] == 1:
                priceBigvolPriceIndexs.append(resultEnd[i][0])
                bigVolPrice[resultEnd[i][0]] = 1
            if resultEnd[i][6]==1:
                myUp[resultEnd[i][0]] = 1

        # 主力散户反转信号
        iList = []
        zList = []
        sList = []
        fList = []
        zsm = {}
        for index, row in result.iterrows():
            iList.append(index - self.queryStock.start)
            z = float(row['z'])
            s = float(float(row['s']))
            zList.append(z)
            sList.append(s)
            convert = int(row['m'])
            if convert == 1:
                fList.append(index - self.queryStock.start)
            if z > s and convert == 1:
                zsm[index - self.queryStock.start] = 1

        myResult = pd.DataFrame()
        myResult['tprice'] = p
        tianjingle = self.least.everyErChengPriceForArray(np.array(x), np.array(p), 30)
        x1 = []
        y1 = []
        if tianjingle == None:
            return
        for item in tianjingle:
            kX = item[0]
            kk = item[1]
            x1.append(kX)
            y1.append(kk)
        pingjunchengbendic = dict(zip(x1, y1))
        self.draw.ax3Show(x1, y1, 'r', '一阶导数')

        oldTwok = 0
        oldOne = 0
        # 牛顿策略
        NewtonBuySall = []
        downlimitTemp = 0

        # 回测的缓存数据
        buyList = []
        sellList = []
        total = len(result)
        for i in range(len(erjieK)):
            item = erjieK[i]
            currentx = item[0]
            twok = item[1]
            downParent = item[2]
            onek = yijiedict.get(currentx)
            onkslow = yijieSlowdict.get(currentx)
            onkchengben = pingjunchengbendic.get(currentx)
            buyTemp = []
            sellTemp = []
            if onek == None or onkslow == None or onkchengben == None:
                continue
            if onkslow < 0 and onkchengben < 0:
                onslowyestaday = yijieSlowdict.get(currentx - 1)
                chengbenyestaday = pingjunchengbendic.get(currentx - 1)
                if onslowyestaday == None or chengbenyestaday == None:
                    continue
                if onslowyestaday < 0 and chengbenyestaday < 0 and onslowyestaday < onkslow and onkchengben < chengbenyestaday:
                    buyTemp.append(currentx)
                    buyTemp.append(twok)
                    buyTemp.append("g")
                    #筹码的上涨动力要足
                    if bigVolPrice.__contains__(currentx) and myUp.__contains__(currentx):
                        buyTemp.append(1)
                    else:
                        buyTemp.append(0)
                    buyList.append(buyTemp)
                    if currentx == total - 1:
                        self.avgCostGrad = onkchengben

            # 一阶导数大于0，二阶导数大于0，一阶导数大于二阶导数，二阶导数递减
            if oldTwok > 0 and oldOne > 0 and oldTwok >= oldOne and onek > 0 and onek > twok:
                sellTemp.append(currentx)
                sellTemp.append(twok)
                sellTemp.append("r")
                sellList.append(sellTemp)
            if oldOne > 0 and onek > 0 and oldOne > onek and oldTwok > oldOne and onek > twok:
                # 添加历史回测里
                sellTemp.append(currentx)
                sellTemp.append(twok)
                sellTemp.append("r")
                sellList.append(sellTemp)
            if onek > 0 and oldOne < 0:
                # 添加历史回测里
                sellTemp.append(currentx)
                sellTemp.append(twok)
                sellTemp.append("orange")
                sellList.append(sellTemp)
            # 一阶导数小于0，二阶导数小于0,一阶导数小于二阶导数，二阶导数递增,并且在之前的三天都被一阶导数压制
            if onek <= 0 and twok > onek and oldTwok < oldOne and downParent < self.downlimit and abs(
                    twok - oldTwok) > abs(
                    onek - oldOne):
                # 添加到历史回测里
                buyTemp.append(currentx)
                buyTemp.append(twok)
                buyTemp.append("g")
                if bigVolPrice.__contains__(currentx):
                    buyTemp.append(1)
                else:
                    buyTemp.append(0)
                buyList.append(buyTemp)
            oldTwok = twok
            oldOne = onek

        # 画线条
        self.draw.klineInfo(buyList, sellList)

        # 找到最小的那一个
        for item in erjieK:
            if item[1] != None and item[1] < downlimitTemp:
                downlimitTemp = item[1]
        downlimitTemp = abs(downlimitTemp)
        self.draw.drawDownLine(abs(downlimitTemp) * (self.downlimit / 100))
        for item in erjieK:
            item[2] = item[1] / downlimitTemp * 100
        # self.loopBack.testNewTon(NewtonBuySall,self.indexCloseDict)
        # self.draw.ax5Show(self.loopBack.baseRmb,self.loopBack.buysell,self.loopBack.myRmb)
        self.draw.ax5ShowZsm(zsm, fList, priceBigvolPriceIndexs, iList, zList, sList)

        self.draw.savePng()
        return self
