import os

from matplotlib import colors as mcolors  # 用于颜色转换成渲染时顶点需要的颜色格式
from matplotlib.collections import LineCollection, PolyCollection  # 用于绘制直线集合和多边形集合
import matplotlib.ticker as ticker  # 用于日期刻度定制
import talib
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor  # 处理鼠标


class DrawPictureReal:


    matix=[]
    date_tickers = []
    isShow=True
    ax1=None
    ax2=None
    ax3=None
    ax4=None
    ax5=None
    xdates=[]
    code=''
    savePath=''


    # 绘制蜡烛图
    def format_date(self, x, pos=None):
        # 日期格式化函数，根据天数索引取出日期值
        return '' if x < 0 or x > len(self.date_tickers) - 1 else self.date_tickers[int(x)]


    def showK(self ,code,result ,isShow,savePath):
        savePath = savePath.strip()+"\\temp"
        self.savePath=savePath.rstrip("\\")
        self.isTest=False
        self.isShow=isShow
        self.code=code
        t3Price = talib.T3(result['close'], timeperiod=30, vfactor=0)
        self.date_tickers=result.date.values
        result.date = range(0, len(result))  # 日期改变成序号
        self.matix = result.values  # 转换成绘制蜡烛图需要的数据格式(date, open, close, high, low, volume)
        xdates = self.matix[:, 0]  # X轴数据(这里用的天数索引)
        if isShow:
            # 设置外观效果
            plt.rc('font', family='Microsoft YaHei')  # 用中文字体，防止中文显示不出来
            plt.rc('figure', fc='k')  # 绘图对象背景图
            plt.rc('text', c='#800000')  # 文本颜色
            plt.rc('axes', axisbelow=True, xmargin=0, fc='k', ec='#800000', lw=1.5, labelcolor='#800000',
                   unicode_minus=False)  # 坐标轴属性(置底，左边无空隙，背景色，边框色，线宽，文本颜色，中文负号修正)
            plt.rc('xtick', c='#d43221')  # x轴刻度文字颜色
            plt.rc('ytick', c='#d43221')  # y轴刻度文字颜色
            plt.rc('grid', c='#800000', alpha=0.9, ls=':', lw=0.8)  # 网格属性(颜色，透明值，线条样式，线宽)
            plt.rc('lines', lw=0.8)  # 全局线宽
            fig = plt.figure(figsize=(16, 8))
            left, width = 0.05, 0.9
            self.ax1 = fig.add_axes([left, 0.5, width, 0.48])  # left, bottom, width, height
            self.ax2 = fig.add_axes([left, 0.4, width, 0.1], sharex=self.ax1)  # 共享ax1轴
            self.ax3 = fig.add_axes([left, 0.3, width, 0.09], sharex=self.ax1)  # 共享ax1轴
            self.ax4 = fig.add_axes([left, 0.2, width, 0.09], sharex=self.ax1)  # 共享ax1轴
            self.ax5 = fig.add_axes([left, 0.1, width, 0.09], sharex=self.ax1)  # 共享ax1轴
            plt.setp(self.ax1.get_xticklabels(), visible=True)  # 使x轴刻度文本不可见，因为共享，不需要显示
            plt.setp(self.ax2.get_xticklabels(), visible=True)  # 使x轴刻度文本不可见，因为共享，不需要显示
            self.ax1.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date))  # 设置自定义x轴格式化日期函数
            self.ax1.xaxis.set_major_locator(ticker.MultipleLocator(max(int(len(result) / 15), 5)))  # 横向最多排15个左右的日期，最少5个，防止日期太拥挤
            # # 下面这一段代码，替换了上面注释的这个函数，因为上面的这个函数达不到同花顺的效果
            opens, closes, highs, lows = self.matix[:, 1], self.matix[:, 4], self.matix[:, 2], self.matix[:, 3]  # 取出ochl值
            avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))  # 计算每个日期之间的距离
            delta = avg_dist_between_points / 4.0  # 用于K线实体(矩形)的偏移坐标计算
            barVerts = [((date - delta, open), (date - delta, close), (date + delta, close), (date + delta, open)) for date, open, close in zip(xdates, opens, closes)]  # 生成K线实体(矩形)的4个顶点坐标
            rangeSegLow = [((date, low), (date, min(open, close))) for date, low, open, close in  zip(xdates, lows, opens, closes)]  # 生成下影线顶点列表
            rangeSegHigh = [((date, high), (date, max(open, close))) for date, high, open, close in zip(xdates, highs, opens, closes)]  # 生成上影线顶点列表
            rangeSegments = rangeSegLow + rangeSegHigh  # 上下影线顶点列表
            cmap = {
                True: mcolors.to_rgba('#000000', 1.0),
                False: mcolors.to_rgba('#54fcfc', 1.0)
            }  # K线实体(矩形)中间的背景色(True是上涨颜色，False是下跌颜色)
            inner_colors = [cmap[opn < cls] for opn, cls in zip(opens, closes)]  # K线实体(矩形)中间的背景色列表
            cmap = {True: mcolors.to_rgba('#ff3232', 1.0),
                    False: mcolors.to_rgba('#54fcfc', 1.0)}  # K线实体(矩形)边框线颜色(上下影线和后面的成交量颜色也共用)
            updown_colors = [cmap[opn < cls] for opn, cls in zip(opens, closes)]  # K线实体(矩形)边框线颜色(上下影线和后面的成交量颜色也共用)列表
            #
            self.ax1.add_collection(LineCollection(rangeSegments, colors=updown_colors, linewidths=0.5 ,antialiaseds=False))
            # 生成上下影线的顶点数据(颜色，线宽，反锯齿，反锯齿关闭好像没效果)
            self.ax1.add_collection(PolyCollection(barVerts, facecolors=inner_colors, edgecolors=updown_colors, antialiaseds=False
                               ,linewidths=0.5))
            # 生成多边形(矩形)顶点数据(背景填充色，边框色，反锯齿，线宽)

            # 绘制均线
            mav_colors = ['#ffffff', '#d4ff07', '#ff80ff', '#00e600', '#02e2f4', '#ffffb9', '#2a6848']  # 均线循环颜色
            mav_period = [5, 10, 20, 30, 60, 120, 180]  # 定义要绘制的均线周期，可增减
            n = len(result)
            for i in range(len(mav_period)):
                if n >= mav_period[i]:
                    mav_vals = result['close'].rolling(mav_period[i]).mean().values
                    self.ax1.plot(xdates, mav_vals, c=mav_colors[i % len(mav_colors)], label='MA' + str(mav_period[i]))
            # 线性回归展示
            # for item in erChengPrice:
            #     myX=item[0]
            #     myY=item[1]
            #     ax1.plot(myX, myY, color="yellow", linewidth=0.3)

            self.ax1.plot(xdates ,t3Price ,label='t3price')
            self.ax1.set_title(code)  # 标题
            self.ax1.grid(True)  # 画网格
            self.ax1.legend(loc='upper left')  # 图例放置于右上角
            self.ax1.xaxis_date()  # 好像要不要效果一样？
        return

    def klineInfo(self,buyList,sellList):
        if self.isShow:
            for item in buyList:
                self.ax2.scatter(item[0], item[1], color=item[2], linewidth=0.0004)
                self.ax1.axvline(item[0], ls='-', color=item[2], lw=0.5)
                if item[3]==1:
                    self.ax1.axvline(item[0], ls='-', c='g', lw=5, ymin=0, ymax=0.02)

            for item in sellList:
                self.ax2.scatter(item[0], item[1], color=item[2], linewidth=0.0004)
                self.ax1.axvline(item[0], ls='-', color=item[2], lw=0.5)
        return

    def drawDownLine(self,downLimit):
        if self.isShow:
            self.ax2.axhline(0, ls='-', c='g', lw=0.5)  # 水平线
            self.ax2.axhline(downLimit, ls='-', c='b', lw=0.5)  # 水平线
            self.ax2.grid(True)  # 画网格
        return

    #填充ax1的数据
    def ax1Show(self,wangX,wangY):
        if self.isShow:
            self.ax2.plot(wangX, wangY, color="w", linewidth=0.6, label='一阶导数')
        return

    #填充ax1的数据
    def ax2Show(self,wangX,wangY):
        if self.isShow:
            self.ax2.plot(wangX, wangY, color="y", linewidth=0.6, label='二阶导数')
        return

    #填充ax1的数据
    def ax3Show(self,x1,y1,c,title):
        if self.isShow:
            self.ax3.plot(x1, y1, color=c, linewidth=0.6, label=title)
        return

    def ax3showSlow(self,wangXSlow, wangYSlow):
        if self.isShow:
            self.ax3.axhline(0, ls='-', c='g', lw=0.5)
            self.ax3.plot(wangXSlow, wangYSlow, color="#33FFff", linewidth=0.6, label='慢速导数')
        return

    #填充ax1的数据
    def ax4Show(self,x,p,priceTwo):
        if self.isShow:
            self.ax4.plot(x, p, c='b', label='移动成本')
            self.ax1.plot(x, p, c='b', label='移动成本')
            self.ax4.plot(self.xdates, priceTwo, c='r', label='jaige')
            self.ax4.grid(True)  # 画网格
        return
    #填充ax1的数据
    def ax5Show(self,baseRmb,buySell,myRmb):
        if self.isShow:
            # self.ax5.axhline(baseRmb, ls='-', c='w', lw=0.5)  # 水平线
            # self.ax5.plot(buySell, myRmb, c='g', label='测试')
            # self.ax5.legend(loc='upper left')  # 图例放置于右上角
            # self.ax5.grid(True)  # 画网格
            # cursor = Cursor(self.ax1, useblit=True, color='w', linewidth=0.5, linestyle='--')
            isExists = os.path.exists(self.savePath)
            # 判断结果
            if not isExists:
                os.makedirs(self.savePath)
            plt.savefig(self.savePath+"\\"+self.code+".png")
            plt.close()
        return

    def ax5ShowZsm(self, zsm, fList, priceBigvolPriceIndexs, iList,zList,sList):
        if self.isShow:
            for c in fList:
                self.ax5.axvline(c, ls='-', c='#ed1941', lw=1)
                self.ax1.axvline(c, ls='-', c='#ed1941', lw=2)

            for i in priceBigvolPriceIndexs:
                if zsm.__contains__(i):
                    self.ax5.axvline(i, ls='-', c='#102b6a', lw=2)
                    self.ax1.axvline(i, ls='-', c='#f47920', ymin=0, ymax=0.02, lw=10)

            self.ax5.plot(iList, zList, c='#6950a1', lw=2, label='主力')
            self.ax5.plot(iList, sList, c='#45b97c', lw=2, label='散户')
            self.ax5.legend(loc='upper left')  # 图例放置于右上角
            self.ax5.grid(True)  # 画网格
    #保存图片
    def savePng(self):
        if self.isShow:
            isExists = os.path.exists(self.savePath)
            # 判断结果
            if not isExists:
                os.makedirs(self.savePath)
            plt.savefig(self.savePath + "\\" + self.code + ".png")
            if self.isTest:
                plt.show()
            plt.close()

    #神仙趋势线
    def shenxianQS(self, testX, H1, H2, H3):
        self.ax4.plot(testX, H1, c="red", label='h1')
        self.ax4.plot(testX, H2, c="green", label='h2')
        self.ax4.plot(testX, H3, c="yellow", label='h3')
        qiangshi=[]
        for i in range(len(testX)):
            if H1[i]!=None and H2[i]!=None and H3[i]!=None:
                if H1[i]>H2[i] and H3[i]<H2[i]:
                    qiangshi.append(i)
                    self.ax1.axvline(i, ls='-', c='red', ymin=0, ymax=0.04, lw=1)
                if H1[i]<H2[i] and H3[i]>H2[i]:
                    self.ax1.axvline(i, ls='-', c='blue', ymin=0, ymax=0.04, lw=1)
                if H1[i]>H2[i] and H3[i]>H1[i]:
                    self.ax1.axvline(i, ls='-', c='yellow', ymin=0, ymax=0.04, lw=1)
                if H1[i]<H2[i] and H3[i]<H1[i]:
                    self.ax1.axvline(i, ls='-', c='green', ymin=0, ymax=0.04, lw=1)
                if H1[i]>H3[i] and H3[i]>H2[i] or H2[i]>H3[i] and H3[i]>H1[i]:
                    self.ax1.axvline(i, ls='-', c='white', ymin=0, ymax=0.04, lw=1)

        pass
