import akshare as ak

stock_history_dividend_detail_df = ak.stock_history_dividend_detail(symbol="300059", indicator="分红")

for index, row in stock_history_dividend_detail_df.iterrows():
    temp = []
    print(row['除权除息日'])


print("---")
stock_history_dividend_detail_df = ak.stock_history_dividend_detail(symbol="600958", indicator="配股")
print(stock_history_dividend_detail_df)

for index, row in stock_history_dividend_detail_df.iterrows():
    temp = []
    print(row['缴款终止日'])
