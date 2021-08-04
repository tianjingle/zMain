import json
import uuid

import pymysql
import requests
from prettytable import PrettyTable

from src.NewTun.Connection import Connection


class JgdyQuery:


    connection = None
    cursor = None
    #解析数据
    def __init__(self):
        self.connection = Connection()
        # print(self.connection.jgdyUrl)

    #解析数据
    def printJgdyInfo(self,code,page):
        url = self.connection.jgdyUrl
        url=url.format(code,page,10,page)
        # print(url)
        datas = self.get_url(url)

        # 取出json部门
        datas = datas[datas.find('{'):datas.find('}') + 3]  # 从出现第一个{开始，取到}
        jsonBody = json.loads(datas)
        jsonDatas = jsonBody['Data']
        realData=jsonDatas[0]
        # pages=realData['TotalPage']
        splitStr=realData["SplitSymbol"]
        FieldName=realData["FieldName"]
        # print(FieldName)
        FieldNames=FieldName.split(',')
        # print(len(FieldNames))
        myData=realData['Data']
        # table = PrettyTable()
        # table.field_names = FieldNames
        fundsArray=[]
        # print(len(myData))
        current=[]
        i=0
        for data in myData:
            fundsArray = data.split(splitStr)
            if i<3:
                current.append(fundsArray)
                i=i+1
            # print(fundsArray)
            # table.add_row(fundsArray)
            self.save2DB(fundsArray)
        return current
        # return table

    #获取数据
    def get_url(self, url, params=None, proxies=None):
        rsp = requests.get(url, params=params, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text

    def save2DB(self,item):
        connect = pymysql.Connect(
            host=self.connection.host,
            port=self.connection.port,
            user=self.connection.user,
            passwd=self.connection.passwd,
            db=self.connection.db,
            charset=self.connection.charset
        )
        cursor=connect.cursor()
        sql = "select * from ajgdy where CompanyCode='%s' and Licostaff='%s' and NoticeDate='%s'"
        data = (item[0], item[15],item[7])
        cursor.execute(sql % data)
        if len(list(cursor)) == 0:
            # print(item)
            sql = "INSERT INTO ajgdy (id, CompanyCode,CompanyName,OrgCode,OrgName,OrgSum,SCode,SName,NoticeDate,StartDate,EndDate,Place,Description,Orgtype,OrgtypeName,Personnel,Licostaff,Maincontent,ChangeP,Close) " \
                  "VALUES ( '%s', '%s','%s', '%s','%s', '%s', '%s','%s', '%s','%s','%s', '%s','%s', '%s','%s', '%s', '%s','%s', '%s','%s')"
            data = (uuid.uuid1(), item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],item[8], item[9], item[10], item[11],item[12], item[13], item[14], item[15],item[16], item[17], item[18])
            cursor.execute(sql % data)
            connect.commit()


    def queryAllByDate(self,startDate):
        result=[]
        sql = "select scode,sname,startDate from ajgdy where startdate>'"+startDate+"'"
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset,
            sql_mode="STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
        )
        # 获取游标
        cursor = connect.cursor()
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[0])
            temp.append(row[1])
            temp.append(row[2])
            result.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return result

# tianjl = JgdyQuery()
# tianjl.printJgdyInfo("300232",1)
