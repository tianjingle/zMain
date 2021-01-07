import time

from src.NewTun.QueryStock import QueryStock


class Statistics:


    def fetchStocks(self):
        query = QueryStock()
        codeList = query.queryHistoryStock()
        for item in codeList:
            #拿到基期和当前时间的价格
            priceList=query.fetchPriceList(item[1],item[3])
            #利益差额的百分比
            profit=(float(priceList[1][0])-float(priceList[0][0]))*100/float(priceList[0][0])
            #更新数据库
            query.updateCandidate(item[0],priceList[0][0],priceList[1][0],profit,priceList[1][1])




