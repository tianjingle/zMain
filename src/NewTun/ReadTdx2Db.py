import csv
import os

class ReadTdx2Db:

    def readData(self,path,start,end):
        temp=[]
        if os.path.exists(path)==False:
            return temp
        with open(path) as csvFile:
            readcsv = csv.reader(csvFile)
            rows = [row for row in readcsv]
            for row in rows:
                if row[0]!='date' and row[0]>=start and row[0]<=end:
                    temp.append(row)
        return temp
