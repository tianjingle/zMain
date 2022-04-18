import json

import easyquotation

quotation = easyquotation.use('tencent') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

#获取所有股票行情
# a=quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
# print(a)
#单只股票
b=quotation.real('sz000009') # 支持直接指定前缀，如 'sh000001'
print(type(b))
print(b['000009']['now'])
print("\n")
#多只股票
c=quotation.stocks(['sz000009', '162411'])
print(c)

#同时获取指数和行情
quotation.stocks(['sh000001', 'sz000001'], prefix=True)