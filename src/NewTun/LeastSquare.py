#线性回归
from scipy.optimize import leastsq
import numpy as np

class LeastSquare:


    erChengPrice=[]


    ##需要拟合的函数func :指定函数的形状 k= 0.42116973935 b= -8.28830260655
    def func(self,p, x):
        k, b = p
        return k * x + b


    ##偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
    def error(self,p, x, y):
        return self.func(p, x) - y


    #计算二乘价格
    def everyErChengPrice(self,sourceResult1,step,isProd):
        # k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
        window=step+3
        if isProd==False:
            sourceResult=sourceResult1[-window:]
        else:
            sourceResult = sourceResult1
        Kflag=[]
        p0=[1,20]
        start=0
        end=0
        #最前的7天都不计算
        count=len(sourceResult)
        if count-step<0:
            return
        for index, row in sourceResult.iterrows():
            temp=[]
            ktemp=[]
            myEnd=index+step
            end=start+step
            if end > count:
                break
            XI=sourceResult.values[start:end][:,0]
            YI=sourceResult['tprice'].astype('float')[start:end]
            # 把error函数中除了p0以外的参数打包到args中(使用要求)
            Para = leastsq(self.error, np.array(p0), args=(XI, YI))
            # 读取结果
            k, b = Para[0]
            temp.append(XI)
            temp.append(k * XI + b)
            #回归的变化率
            ktemp.append(myEnd-1)
            ktemp.append(k)
            Kflag.append(ktemp)
            start=start+1

        # for i in range(count):
        #     temp=[]
        #     ktemp=[]
        #     myStart=i
        #     myEnd=i+step
        #     if myEnd>count:
        #         break
        #     XI=sourceResult.values[myStart:myEnd][:,0]
        #     YI=sourceResult['tprice'].astype('float')[myStart:myEnd]
        #     # 把error函数中除了p0以外的参数打包到args中(使用要求)
        #     Para = leastsq(self.error, np.array(p0), args=(XI, YI))
        #     # 读取结果
        #     k, b = Para[0]
        #     temp.append(XI)
        #     temp.append(k * XI + b)
        #     #回归的变化率
        #     ktemp.append(myEnd)
        #     ktemp.append(k)
        #     Kflag.append(ktemp)
        return Kflag

    #通过数组的方式计算二阶导数
    def everyErChengPriceForArray(self,sourceX,sourceY,step):
        # k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
        Kflag=[]
        p0=[1,20]
        #最前的7天都不计算
        count=len(sourceX)
        if count-step<0:
            return
        for i in range(count):
            temp=[]
            ktemp=[]
            myStart=i
            myEnd=i+step
            if myEnd>count:
                break
            XI=sourceX[myStart:myEnd]
            YI=sourceY[myStart:myEnd]
            # 把error函数中除了p0以外的参数打包到args中(使用要求)
            Para = leastsq(self.error, np.array(p0), args=(XI, YI))
            # 读取结果
            k, b = Para[0]
            temp.append(XI)
            temp.append(k * XI + b)
            self.erChengPrice.append(temp)
            #回归的变化率
            ktemp.append(sourceX[myEnd-1])
            ktemp.append(k)
            Kflag.append(ktemp)
        return Kflag

    #二阶导数
    def doubleErJie(self,yijieList,step,isProd):
        erjieK=[]
        # k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
        p0 = [1, 20]
        # 最前的7天都不计算
        count = len(yijieList)
        if count - step < 0:
            return
        start=yijieList[0][0]
        for i in range(count):
            end=0
            ktemp = []
            myEnd = i + step
            if myEnd > count:
                break
            tempX=[]
            tempY=[]
            for j in range(step):
                end=yijieList[i+j][0]
                tempX.append(yijieList[i+j][0]-start)
                tempY.append(yijieList[i+j][1])
            # 把error函数中除了p0以外的参数打包到args中(使用要求)
            Para = leastsq(self.error, np.array(p0), args=(np.array(tempX), np.array(tempY)))
            # 读取结果
            k, b = Para[0]
            # 回归的变化率
            ktemp.append(end)
            ktemp.append(k*5)
            ktemp.append(0)
            erjieK.append(ktemp)
        return erjieK