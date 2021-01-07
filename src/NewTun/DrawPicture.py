class DrawPicture:


    matix=[]
    date_tickers = []
    isShow=False
    ax1=None
    ax2=None
    ax3=None
    ax4=None
    ax5=None
    xdates=[]
    code=''


    # 绘制蜡烛图
    def format_date(self, x, pos=None):
        # 日期格式化函数，根据天数索引取出日期值
        return '' if x < 0 or x > len(self.date_tickers) - 1 else self.date_tickers[int(x)]


    def showK(self ,code,result ,isShow):
        if self.isShow:
            print(1)
        return

    def klineInfo(self,buyList,sellList):
        if self.isShow:
            print(1)
        return


    def drawDownLine(self,downLimit):
        if self.isShow:
            print(1)
        return



    #填充ax1的数据
    def ax1Show(self,wangX,wangY):
        if self.isShow:
            print(1)
        return



    #填充ax1的数据
    def ax2Show(self,wangX,wangY):
        if self.isShow:
            print(1)
        return



    #填充ax1的数据
    def ax3Show(self,x1,y1,c,title):
        if self.isShow:
            print(1)
        return

    def ax3showSlow(self,wangXSlow, wangYSlow):
        if self.isShow:
            print(1)
        return

    #填充ax1的数据
    def ax4Show(self,x,p,priceTwo):
        if self.isShow:
            print(1)
        return

    #填充ax1的数据
    def ax5Show(self,baseRmb,buySell,myRmb):
        if self.isShow:
            print(1)
        return