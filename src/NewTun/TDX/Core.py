from src.NewTun.TDX.AutoDownload import AutoDownload


#通达信自动化获取数据及数据加工
from src.NewTun.TDX.readTDX_cw import readTDX_cw
from src.NewTun.TDX.readTDX_lday import readTDX_lday


class Core:

    def exec(self):
        # tdxdownload=AutoDownload()
        #下载日线数据，以及财务数据
        # tdxdownload.autoDownload()
        #gbbq
        a=readTDX_cw()
        a.parseCW()
        #讲下载的数据进行二次计算，然后放到指定的目录，等待zMain处理
        # b=readTDX_lday()
        # b.execute()

# Core().exec()