import json
import os
import akshare as ak


class Industry:

    # 板块文件地址
    BANKUAN_CODE_PATH = os.path.join(os.path.dirname(__file__), "Industry_name.conf")

    # 更新板块code
    def update_bankuan(self):
        result=ak.stock_board_industry_name_em()
        IndustryNames=[]
        for index, row in result.iterrows():
            IndustryNames.append(row['板块名称'])
        with open(self.BANKUAN_CODE_PATH, "w") as f:
            f.write(json.dumps(dict(stock=IndustryNames)))
        return IndustryNames

    # 加载板块代码文件
    def get_bankuan_names(self,realtime=False):
        if realtime:
            return self.update_bankuan()
        with open(self.BANKUAN_CODE_PATH) as f:
            return json.load(f)["stock"]

    def get_bankuan_day_line(self,name):
        result=ak.stock_board_industry_hist_em(symbol=name,adjust="")
        return result


# result=Industry().get_bankuan_names()
# print(result)
# for item in result:
#     a=Industry().get_bankuan_day_line(item)
#     print(a)