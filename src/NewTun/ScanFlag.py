
class ScanFlag:

    stockIndex='stockIndex'
    baseIndex=0

    def readIndex(self,today):
        fi=open(self.stockIndex,"r",encoding="utf-8")
        index=fi.readlines()
        if len(index)!=0 and index[0].strip()!='' and index[0].startswith(today):
            self.baseIndex=index[0].split("_")[1]
        else:
            self.baseIndex=0
        return self.baseIndex

    def writeIndex(self,today,nowIndex):
        fi = open(self.stockIndex, "w", encoding="utf-8")
        fi.write(str(today+"_"+str(nowIndex)))
        fi.close()