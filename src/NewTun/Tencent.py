import easyquotation

#获取实时股票价格
class Tencent:

    quotation = easyquotation.use('tencent') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

    def getCurrentStockInfo(self,code):
        #单只股票
        code=code.upper()
        code=code.replace("SZ","")
        code=code.replace("SH","")
        code=code.replace(".","")
        b=self.quotation.real(code) # 支持直接指定前缀，如 'sh000001'
        print(b)
        return b[code]

# now=Tencent().getCurrentStockInfo("600260")
# print(str(now['datetime']).split(" ")[0])
