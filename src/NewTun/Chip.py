class Chip:

    index=0

    open=0

    close=0

    max=0

    min=0

    avc_price=0

    chouMa=0

    def __init__(self,index,open,close,max,min,avc_price,chouMa):
        self.index=index
        self.open=open
        self.close=close
        self.max=max
        self.min=min
        self.avc_price=avc_price
        self.chouMa=chouMa

    def getChouMa(self):
        return self.chouMa


    def getOpen(self):
        return self.open

    def getClose(self):
        return self.close

    def getAvcPrice(self):
        return self.avc_price

    def getMax(self):
        return self.max

    def getMin(self):
        return self.min

    def getIndex(self):
        return self.index

    def print(self):
        print("日期："+str(self.getIndex())+"    筹码："+str(self.getChouMa())+"    最高："+str(self.getMax())+"    最低："+str(self.getMin())+"    平均："+str(self.getAvcPrice()))