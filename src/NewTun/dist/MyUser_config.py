import os


class user_config:
    # 配置部分开始
    debug = False  # 是否开启调试日志输出  开=True  关=False
    basePath="C:\\zMain-pic"

    # 目录需要事先手动建立好，不然程序会出错
    tdx = {
        'tdx':"C:\\new_jyplug",
        'tdx_path': basePath,  # 指定通达信目录
        'csv_cw': basePath+'\\vipdoc\\cw',  # 指定专业财务保存目录
        'csv_gbbq': basePath+'\\',  # 指定股本变迁保存目录
        'pytdx_ip': '218.6.170.55',  # 指定pytdx的通达信服务器IP
        'pytdx_port': 7709,  # 指定pytdx的通达信服务器端口。int类型
    }

    index_list = [  # 通达信需要转换的指数文件。通达信按998查看重要指数
        'sh999999.day',  # 上证指数
        'sh000300.day',  # 沪深300
        'sz399001.day',  # 深成指
    ]

    def __init__(self):
        path=self.tdx['tdx_path'] + os.sep + "vipdoc" + os.sep + "cw"
        if not os.path.exists(path):
            os.makedirs(path)

