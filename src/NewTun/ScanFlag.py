import os
import time


class ScanFlag:


    # 板块文件地址
    stockIndex = os.path.join(os.path.dirname(__file__), "stockIndex")
    fanzhuanIndex = os.path.join(os.path.dirname(__file__), "fanzhuan")

    baseIndex=0

    def readIndex(self,i,today):
        fi=open(self.stockIndex+str(i),"r",encoding="utf-8")
        index=fi.readlines()
        if len(index)!=0 and index[0].strip()!='' and index[0].startswith(today):
            self.baseIndex=index[0].split("_")[1]
        else:
            self.baseIndex=0
        return self.baseIndex

    def writeIndex(self,i,today,nowIndex):
        fi = open(self.stockIndex+str(i), "w", encoding="utf-8")
        fi.write(str(today+"_"+str(nowIndex)))
        fi.close()

    def resetFanzhuan(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.writeFanzhuanIndex(today,0)

    #fanzhuan+1
    def addFanzhuan2File(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fdate,nowCount=self.readFanzhuanIndex()
        self.writeFanzhuanIndex(today,nowCount+1)

    def readFanzhuanIndex(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fi=open(self.fanzhuanIndex,"r",encoding="utf-8")
        index=fi.readlines()
        if len(index)!=0 and index[0].strip()!='' and index[0].startswith(today):
            fdate=index[0].split("_")[0]
            ftotal=index[0].split("_")[1]
            return fdate,int(ftotal)
        else:
            return today,0


    def writeFanzhuanIndex(self,today,nowIndex):
        fi = open(self.fanzhuanIndex, "w", encoding="utf-8")
        fi.write(str(today+"_"+str(nowIndex)))
        fi.close()