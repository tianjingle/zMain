# 突然觉醒
import uuid

import pymysql

from src.NewTun.Application import Application
from src.NewTun.Connection import Connection
from src.NewTun.QueryStock import QueryStock
from src.NewTun.StockInfoSyn import StockInfoSyn

class DongliFanzhuan:

    def donglifanzhuan(self):
        query = QueryStock()
        today = query.todayIsTrue()[0]
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        # 获取游标
        cursor = connect.cursor()
        print("-----------------------------scan dongli fanzhuan------------------------------------")
        syn = StockInfoSyn()
        basicStock = syn.getBiscicStock()
        for i in range(len(basicStock)):
            item = basicStock[i]
            test = Application()
            kk = test.executeForFanzhuanDongli(basicStock[i][0])
            if kk.isZsm == 99:
                # 插入数据
                sql = "select * from candidate_stock where code='%s' and collect_date='%s'"
                data = (item[0], today)
                cursor.execute(sql % data)
                if len(list(cursor)) == 0:
                    print(item)
                    sql = "INSERT INTO candidate_stock (id, code, name,collect_date,industry,grad,cv,is_down_line,zsm) VALUES ( '%s', '%s','%s', '%s','%s', %.8f, %.8f,%i,%i)"
                    data = (uuid.uuid1(), item[0], item[1], today, item[3], test.avgCostGrad, abs(test.cvValue),
                            test.isDownLine, kk.isZsm)
                    cursor.execute(sql % data)
                    connect.commit()
            # 垃圾回收
            del kk, test
        print("动力反转 扫描---finish...")
        pass

