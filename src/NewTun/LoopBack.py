

class LoopBack:

    totalRmb=2000
    baseRmb=totalRmb
    handTotal=0
    buysell=[]
    myRmb=[]

    def testNewTon(self ,NewtonBuySall ,indexCloseDict):
        for item in NewtonBuySall:
            if indexCloseDict.get(item[0 ] +1 )!= None:
                price = float(indexCloseDict.get(item[0 ] +1))
            else:
                continue
            # 买入
            print("当前价格 " +str(price))
            if item[1] == 1:
                currentRmb = price * 100 * 1.002
                if self.totalRmb - currentRmb > 0:
                    self.totalRmb = self.totalRmb - currentRmb
                    self.handTotal = self.handTotal + 1
                    self.buysell.append(item[0])
                    self.myRmb.append(self.totalRmb + self.handTotal * 100 * price)
                    print("总金额：" + str(self.totalRmb) + "   总手数" + str(self.handTotal) + "   账户总金额：" + str(
                        self.totalRmb + self.handTotal * 100 * price))
                    self.finalRmb =self.totalRmb + self.handTotal * 100 * price
                else:
                    self.buysell.append(item[0])
                    self.myRmb.append(self.totalRmb + self.handTotal * 100 * price)
                    print("资金不足")
            elif item[1] == -1:
                if self.handTotal > 0:
                    currentRmb = self.handTotal * 100 * price * 0.998
                    self.totalRmb = self.totalRmb + currentRmb
                    self.buysell.append(item[0])
                    self.myRmb.append(self.totalRmb)
                    self.handTotal = 0
                    print("总金额：" + str(self.totalRmb) + "   总手数" + str(self.handTotal) + "   账户总金额：" + str(self.totalRmb))
                    self.finalRmb =self.totalRmb
                else:
                    self.buysell.append(item[0])
                    self.myRmb.append(self.totalRmb)
                    self.finalRmb =self.totalRmb
                    print("不用再往出卖了")