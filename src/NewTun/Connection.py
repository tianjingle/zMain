import configparser
import os.path

class Connection:

    host = 'localhost'
    port = 3306
    user = 'root'
    passwd = 'tianjingle'
    db = 'noun'
    charset = 'utf8'

    emailPass=''
    emaialUser=''
    sender=''
    receivers=''

    jgdyUrl=''
    syn=False
    isJgdy=False
    scans=2000
    savePath=''
    scanOnlineType="001"

    tdxDayPath=''

    testCode=''
    isTest=False

    def __init__(self):

        cf = configparser.ConfigParser()
        configPath=os.path.join(os.path.dirname(__file__), "config.ini")
        cf.read(configPath)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        self.emailPass = cf.get("Email","pass")  # 发件人邮箱密码
        self.emaialUser = cf.get("Email","user")  # 收件人邮箱账号，我这边发送给自己
        self.sender = cf.get("Email","sender")
        self.receivers = cf.get("Email","receiver")# 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        self.host = cf.get("Mysql-Database", "host")  # 获取[Mysql-Database]中host对应的值
        self.user = cf.get("Mysql-Database", "user")  # 获取[Mysql-Database]中host对应的值
        self.passwd = cf.get("Mysql-Database", "passwd")  # 获取[Mysql-Database]中host对应的值
        self.db = cf.get("Mysql-Database", "db")  # 获取[Mysql-Database]中host对应的值
        self.charset = cf.get("Mysql-Database", "charset")  # 获取[Mysql-Database]中host对应的值
        self.syn=cf.get("System","syn")
        self.scans=cf.get("System","scans")
        self.scanOnlineType=cf.get("System","scanOnlineType")
        self.jgdyUrl=cf.get("Jgdy","fetchUrl")
        self.isJgdy=cf.get("Jgdy","isJgdy")
        self.savePath=cf.get("Path","savePath")
        self.tdxDayPath=cf.get("Path","tdxDayPath")

        if self.scanOnlineType=="001" or self.scanOnlineType=="011" or self.scanOnlineType=="010":
            self.scanOnlineType=self.scanOnlineType
        else:
            self.scanOnlineType="001"

        testCode=cf.get('Test','testCode')
        if testCode!='':
            self.testCode=testCode
            self.isTest=True
        else:
            self.isTest=False