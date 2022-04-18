
class ScanFlag:

    stockIndex='C:\\Users\\Administrator\\PycharmProjects\\zMain\\src\\NewTun\\stockIndex'
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