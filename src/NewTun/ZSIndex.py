import pandas as pd

#主力和散户线
#趋势反转线
class ZSIndex:

    # 在k线基础上计算KDF，并将结果存储在df上面(k,d,j)
    def zsLine(self,df):
        df = df.astype({'low': 'float', 'close': 'float', 'high': 'float'})
        low_list = df['low'].rolling(34, min_periods=9).min()
        low_list.fillna(value=df['low'].expanding().min(), inplace=True)
        high_list = df['high'].rolling(34, min_periods=9).max()
        high_list.fillna(value=df['high'].expanding().max(), inplace=True)
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
        df['d'] = df['k'].ewm(com=2).mean()
        df['j'] = 3 * df['k'] - 2 * df['d']
        # 主力线
        zz = pd.Series.ewm(df['j'], com=2.5).mean()
        # 计算散户线代码：
        low_list1 = df['low'].rolling(55, min_periods=9).min()
        low_list1.fillna(value=df['low'].expanding().min(), inplace=True)
        high_list1 = df['high'].rolling(55, min_periods=9).max()
        high_list1.fillna(value=df['high'].expanding().max(), inplace=True)
        # 散户线
        ss = (high_list1 - df['close']) / ((high_list1 - low_list1)) * 100
        return zz, ss

    # 判断反转信号代码：
    def convertXQH(self,df):
        df = df.astype({'low': 'float', 'close': 'float', 'high': 'float'})
        low_list2 = df['low'].rolling(9, min_periods=9).min()
        low_list2.fillna(value=df['low'].expanding().min(), inplace=True)
        high_list2 = df['high'].rolling(9, min_periods=9).max()
        high_list2.fillna(value=df['high'].expanding().max(), inplace=True)
        rsv1 = (df['close'] - low_list2) / (high_list2 - low_list2) * 50
        df['K1'] = pd.Series.ewm(rsv1, com=2).mean()
        df['D1'] = pd.Series.ewm(df['K1'], com=2).mean()
        df['J1'] = 3 * df['K1'] - 2 * df['D1']
        # stock_datas['M'] =(stock_datas['J1']>3)&
        df['J2'] = df['J1'].shift(1)
        # 是否反转，1表示反转，0表示没有反转
        mm = (df['J1'] > 3) & (df['J2'] <= 3)
        return mm