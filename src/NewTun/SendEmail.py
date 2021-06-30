import os
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from src.NewTun.Connection import Connection
from src.NewTun.JingJu import JingJu
from src.NewTun.QueryStock import QueryStock


class SendEmail:
    tendown=[]
    other=[]
    Zsm=[]
    jingju=JingJu()


    def sendYouCanBuy(self,currentPath):
        query=QueryStock()
        codes=query.queryYouCanBuyStock()
        print(codes)
        self.tendown=[]
        self.other=[]
        for item in codes:
            temp=[]
            price=query.todayKlineByCode(item[0])
            temp.append(item[0])
            temp.append(item[1])
            temp.append(item[4])
            temp.append(item[5])
            temp.append(price)
            if price<=10:
                self.tendown.append(temp)
            else:
                self.other.append(temp)
            #主力、散户、反转信号
            if item[5]==1 or item[5]==2:
                self.Zsm.append(temp)

        self.tendown=sorted(self.tendown, key=lambda s: s[2],reverse=False)
        self.other=sorted(self.other, key=lambda s: s[2],reverse=False)
        self.Zsm=sorted(self.Zsm, key=lambda s: s[3],reverse=True)
        self.doSendStockInfoBeautiful(self.Zsm,currentPath,"回踩反弹股票")
        self.doSendStatisticForZsm()
        self.doSendStockInfoBeautiful(self.tendown,currentPath,"低价股票")
        self.doSendStockInfoBeautiful(self.other,currentPath,"高价股票")
        self.doSendStatisticPaper()

    def getJingjuNext(self):
        return self.jingju.readOneJinju()

    def doSendStockInfoBeautiful(self,codes,currentPath,subject):
        con=Connection()
        myContent="<h4><font color = 'red' > " + self.getJingjuNext() + " </font ></h4></br>"
        imgsOKstr = myContent+"<p>股票总计："+str(len(codes))
        count=80
        #前二十的股票提供图片显示
        for item in codes:
            if count>0:
                imgsOKstr = imgsOKstr + "<p>" + str(item[0]) + "&nbsp;"+str(item[1])+"&nbsp;&nbsp;"+str(item[2])+"&nbsp;&nbsp;"+str(item[3])+"&nbsp;<img src='cid:"+item[0]+"'></p>"
            else:
                imgsOKstr = imgsOKstr + "<p>" + str(item[0]) + "&nbsp;"+str(item[1])+"&nbsp;&nbsp;"+str(item[2])+"&nbsp;&nbsp;"+str(item[3])+"</p>"
            count=count-1

        endDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        my_pass = con.emailPass
        my_user = con.emaialUser
        sender = con.sender
        receivers = con.receivers
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header(str(endDate) + subject, 'utf-8')
        msgRoot['To'] = Header("测试", 'utf-8')
        subject = str(endDate) + subject
        msgRoot['Subject'] = Header(subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = imgsOKstr
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 指定图片为当前目录
        count = 80
        for item in codes:
            if count>0:
                pngPath=currentPath+'\\temp\\' + item[0] + ".png"
                if os.path.exists(pngPath):
                    fp = open(pngPath, 'rb')
                    msgImage = MIMEImage(fp.read())
                    fp.close()
                    temp = "<" + item[0] + ">"
                    # 定义图片 ID，在 HTML 文本中引用
                    msgImage.add_header('Content-ID', temp)
                else:
                    fp = open(currentPath+"\\temp\\zMain.png", 'rb')
                    msgImage = MIMEImage(fp.read())
                    fp.close()
                    temp = "<" + item[0] + ">"
                    # 定义图片 ID，在 HTML 文本中引用
                    msgImage.add_header('Content-ID', temp)
                msgRoot.attach(msgImage)
            count=count-1
        try:
            users=receivers.split(',')
            for item in users:
                smtpObj = smtplib.SMTP()
                smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
                smtpObj.login(my_user, my_pass)
                smtpObj.sendmail(sender, item, msgRoot.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")




    def sendStockInfo(self,codes,currentPath):
        con=Connection()
        myContent="<h4><font color = 'red' > " + self.getJingjuNext() + " </font ></h4></br>"
        imgsOKstr = myContent+"当下可选股票："
        count=60
        #前二十的股票提供图片显示
        for item in codes:
            if count>0:
                imgsOKstr = imgsOKstr + "<p>" + str(item[0]) + "&nbsp;"+str(item[1])+"&nbsp;&nbsp;"+str(item[2])+"&nbsp;&nbsp;"+str(item[3])+"&nbsp;<img src='cid:"+item[0]+"'></p>"
            else:
                imgsOKstr = imgsOKstr + "<p>" + str(item[0]) + "&nbsp;"+str(item[1])+"&nbsp;&nbsp;"+str(item[2])+"</p>"
            count=count-1

        endDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        my_pass = con.emailPass
        my_user = con.emaialUser
        sender = con.sender
        receivers = con.receivers
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header(str(endDate) + " 股票推荐", 'utf-8')
        msgRoot['To'] = Header("测试", 'utf-8')
        subject = str(endDate) + ' 股市有风险，投资需谨慎'
        msgRoot['Subject'] = Header(subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = imgsOKstr
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 指定图片为当前目录
        count = 20
        for item in codes:
            if count>0:
                fp = open(currentPath+'\\temp\\' + item[0] + ".png", 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                temp = "<" + item[0] + ">"
                # 定义图片 ID，在 HTML 文本中引用
                msgImage.add_header('Content-ID', temp)
                msgRoot.attach(msgImage)
            count=count-1
        try:
            users=receivers.split(',')
            for item in users:
                smtpObj = smtplib.SMTP()
                smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
                smtpObj.login(my_user, my_pass)
                smtpObj.sendmail(sender, item, msgRoot.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
    # os.system('shutdown -s -f -t 180')

    #发送统计信息
    def doSendStatisticPaper(self):
        query = QueryStock()
        #暂时统计0.618以下的
        result = query.queryStockYouBrought("is_down_line=1 and profit!=0 and price<=10 and price>3")
        self.sendStatistic(result," zMain吸筹统计")

    #回踩反弹策略历史统计
    def doSendStatisticForZsm(self):
        query = QueryStock()
        result = query.queryStockYouBrought("zsm=1")
        self.sendStatistic(result," 回踩反弹统计")

    # 发送邮件
    def sendStatistic(self,result,title):
        successCount=0
        myContent="<h4><font color = 'red' > " + self.getJingjuNext() + " </font ></h4></br>"
        htmls = myContent+"<table border='1'>"
        htmls=htmls+"<tr><td>代码</td><td>名称</td><td>买入时间</td><td>grad</td><td>cv</td><td>买入价格</td><td>当前价格</td><td>增长幅度100%</td></tr>"
        for item in result:
            htmls=htmls+"<tr>"
            if float(item[7]) > 0:
                successCount = successCount + 1
            for vo in range(len(item)):
                if float(item[7])>0:
                    htmls=htmls+"<td bgcolor='#FFCC66'><font color='red'>" + str(item[vo]) + "</font></td>"
                else:
                    htmls = htmls + "<td bgcolor='#00FF00'><font color='blue'>" + str(item[vo]) + "</font></td>"
            htmls=htmls+"</tr>"
        htmls=htmls+"</table>"
        totalCount=len(result)
        if totalCount==0:
            totalCount=1
        endHtml="增长个数:"+str(successCount)+"&nbsp&nbsp&nbsp&nbsp总共个数："+str(totalCount)+"                </br> 百分比："+str(successCount*100/totalCount)+"%"+htmls
        con = Connection()
        endDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        my_pass = con.emailPass
        my_user = con.emaialUser
        sender = con.sender
        receivers = con.receivers
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header(str(endDate) + " 股票统计", 'utf-8')
        msgRoot['To'] = Header("测试", 'utf-8')
        subject = str(endDate) + title
        msgRoot['Subject'] = Header(subject, 'utf-8')
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = endHtml
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        try:
            users=receivers.split(',')
            for item in users:
                smtpObj = smtplib.SMTP()
                smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
                smtpObj.login(my_user, my_pass)
                smtpObj.sendmail(sender, item, msgRoot.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")



