import pymysql

from src.NewTun.Connection import Connection
from src.NewTun.ScanFlag import ScanFlag


class CacheSaver:


    # cache save to db
    def save(self):
        fdate, nowCount =ScanFlag().readFanzhuanIndex()
        # 获取游标
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        cursor = connect.cursor()
        fanzhuanSql = "select * from a_fan_zhuan_size where collect_date='" + fdate + "'"
        cursor.execute(fanzhuanSql)
        count = len(cursor.fetchall())
        if count >= 1:
            sql="update a_fan_zhuan_size set count="+str(nowCount)+" where collect_date='"+fdate+"' and id!=''"
            print(sql)
            cursor.execute(sql)
            connect.commit()
        cursor.close()
        pass