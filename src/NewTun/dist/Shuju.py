import akshare as ak

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20220519", end_date="20220520", adjust="qfq")
print(stock_zh_a_daily_qfq_df)