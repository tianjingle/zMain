import datetime

import akshare as ak
import pendulum


class Fq:

    list=[]


    def fhpf(self):
        stock_fhps_em_df = ak.stock_fhps_em(date="20211231")
        for index, row in stock_fhps_em_df.iterrows():
            code=str(row['代码'])
            name=str(row['名称'])
            lastday=str(row['除权除息日'])
            if "NaT"==lastday:
                continue
            temp=[]
            temp.append(code)
            temp.append(name)
            t = pendulum.parse(lastday).day_of_week
            dates = lastday.split("-")
            if t==5:
                #如果是星期五复权，那么我们下周一删库，拉数据
                tomorow=self.getday(int(dates[0]),int(dates[1]),int(dates[2]),3)
                if pendulum.parse(tomorow).day_of_week==1:
                    lastday=tomorow
            else:
                #如果星期1到星期4，那就明天删库，拉数据
                lastday=self.getday(int(dates[0]),int(dates[1]),int(dates[2]),1)
            temp.append(lastday)
            self.list.append(temp)
        map = {}
        for item in self.list:
            key = item[0] + "_" + item[2]+"_"+ "drop table " + item[0]
            map[key] = "1"
        return map

    def getday(self,y=2017, m=8, d=15, n=0):
        the_date = datetime.datetime(y, m, d)
        result_date = the_date + datetime.timedelta(days=n)
        d = result_date.strftime('%Y-%m-%d')
        return d


    # 1表示需要进行复权，0表示不需要进行复权
    def todayIsFq(self,code):
        lastDay=""
        code=code.upper()
        code=code.replace("SH","").replace("SZ","").replace(".","")
        print(code)
        #分红
        stock_history_dividend_detail_df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        for index, row in stock_history_dividend_detail_df.iterrows():
            lastDay=str(row['除权除息日'])
            return lastDay

        stock_history_dividend_detail_df = ak.stock_history_dividend_detail(symbol=code, indicator="配股")
        for index, row in stock_history_dividend_detail_df.iterrows():
            lastday=str(row['缴款终止日'])
            return lastDay
        return lastDay

# t=Fq().getday(int(2022),int(5),int(20),3)
# print(t)