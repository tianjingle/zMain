
class ScanFlag:

    stockIndex='stockIndex'
    baseIndex=0

    def readIndex(self):
        fi=open(self.stockIndex,"r",encoding="utf-8")
        index=fi.readlines()
        if len(index)!=0 and index[0].strip()!='':
            self.baseIndex=index[0]
        else:
            self.baseIndex=0
        return self.baseIndex

    def writeIndex(self,nowIndex):
        fi = open(self.stockIndex, "w", encoding="utf-8")
        fi.write(str(nowIndex))
        fi.close()