import math
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

    isZsm=0

    def setStackCode(self):
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
            # temp.append(row['close'])
            temp.append((float(row['high'])+float(row['low']))/2)

            temp.append(row['volume'])
            temp.append(row['tprice'])
            temp.append(row['turn'])
            temp.append(int(row['tradestatus']))
            chipCalculateList.append(temp)
        if isProd==False:
            chipCalculateList=chipCalculateList[-120:]
        calcualate = ChipCalculate()
        resultEnd = calcualate.getDataByShowLine(chipCalculateList,isProd)
        del calcualate
        return resultEnd

    def cv(self,temp):
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
        return result

    #执行器
    def execute(self,code):
        result=self.queryStock.queryStock(code,30)
        if len(result[0])<200:
            return self
        return self.core(result[0],result[1])

    def parseLongli(self,result):
        x=[]
        y=[]
        for index, row in result.iterrows():
            x.append(index)
            a = round(row['DONGLILINE'], 2)
            y.append(float(a))
        today=y[len(y)-1]
        yestoday=y[len(y)-2]
        if today >= 0.2 and yestoday < 0.2:
            return 0.2
        if today > 0.5 and yestoday <= 0.5:
            return 0.5
        if today >= 3.2 and yestoday < 3.2:
            return 3.2
        if today < 3.5 and yestoday >= 3.5:
            return 3.5
        return 0

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
        # lock = threading.Lock()  # 申请一把锁
        # lock.acquire()
        resultEnd = self.chipCalculate(result, self.queryStock.start,False)
        resultEnd.sort(key=lambda resultEnd: resultEnd[0])
        x = []
        p = []
        for i in range(len(resultEnd)):
            x.append(resultEnd[i][0])
            p.append(resultEnd[i][1])

        #最后一天得价格是否大于筹码峰
        bigVolPriceLastOne=resultEnd[len(resultEnd)-1][5]
        myUp=resultEnd[len(resultEnd)-1][6]
        sanJx=resultEnd[len(resultEnd)-1][7]
        currentYasuoXishu=resultEnd[len(resultEnd)-1][8]
        self.cvValue=currentYasuoXishu

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
        z=float(result['z'][len(result) - 1])
        s=float(result['s'][len(result)-1])
        m=float(result['m'][len(result)-1])

        #散户、主力、反转信号
        # print("z="+str(z)+"\ts="+str(s)+"\tm="+str(m)+"\tp>c="+str(resultEnd[len(resultEnd)-1][5]))
        zsmFlag=self.zsmIndexCalculate(z,s,m,resultEnd[len(resultEnd)-1])
        if zsmFlag==1 and sanJx==1:
            self.isZsm=1



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
                        #采用压缩系数替换
                        # self.cvValue = self.cv(choumaList)
                        self.currentPrice=float(result['close'][len(result)-1])
                        if self.currentPrice<=self.maxPrice*0.618:
                            self.isDownLine=1
                        else:
                            self.isDownLine=0
                        if bigVolPriceLastOne == 1 and myUp==1 and sanJx==1:
                            self.isZsm = 2
                        print(self.currentPrice)
                        print(self.maxPrice)
                        print(self.isDownLine)

        self.least=None
        self.loopBack=None
        self.queryStock=None
        return self

    #查看是否符合主力、散户、反转、筹码公式
    def zsmIndexCalculate(self, z,s,m, resultEndLastOne):
        if z>s and m>0 and resultEndLastOne[5]>0:
            return 1
        return 0

    #补充买点
    def executeForFanzhuanDongli(self, code):
        huaerjie = self.queryStock.queryStockFantanFanZhuan(code,1)
        if huaerjie==99:
            self.isZsm=99
            print("动力+反转:\t"+code)
        return self

    #补充买点
    def executeForBc(self, code):
        result = self.queryStock.queryStockBc(code,5)
        if len(result[0]) < 200:
            return self
        type=self.parseLongli(result[0])
        inner=0

        if result[2]>30:
            print(result[2])
            print("好望角买点~")
            self.isZsm=3
        else:
            if type<=0.5 and type!=0 and result[2]>15:
                inner=1
                print("旺角动力~")
                print(result[2])
                self.isZsm=5
        if result[3]>0:
            print("反弹买点~")
            self.isZsm=4
            if type<=0.5 and type!=0:
                inner=1
                print("旺角动力~")
                self.isZsm=5
        if inner==0 and type<=0.5 and type!=0:
            print("纯动力~")
            self.isZsm=6
        if type<=0.5 and type!=0 and result[2]>5 and result[3]>0:
            print("超级+++++：动力，吸筹，反弹")
            self.isZsm = 7
        return self




