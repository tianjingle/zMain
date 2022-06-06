#通达信自动启动下载盘后数据和财务数据
# -*- coding: utf-8 -*-
import subprocess,pyautogui
from time import sleep

class AutoDownload:

    def autoDownload(self):
        pyautogui.PAUSE=1
        pyautogui.FAILSAFE=True
        k=2
        cc=str(pyautogui.size().width)+'*'+str(pyautogui.size().height)
        print("---------------------------通达信自动下载  开始-------------------------------")
        print(cc)
        tdxpt={'buzou':['0免费','1确定','2系统','3盘后数据','4选择日期','5下载','6关闭','7系统','8专业数据','9财务数据','10股票数据','11关闭'],
                  '1440*900':[(858,488),(1000,520),(38,10),(90,260),(420,320),(900,626),(1000,626),(38,10),(90,282),(680,600),(1050,600),(1050,646)],
                  '1920*1080':[(1114,659),(1049,608),(1580,11),(1634,224),(702,402),(1122,709),(1200,700),(38,10),(100,263),(930,670),(1240,670),(1244,716)],
                  '1366*768':[
                      # (854, 502),  #游客 0
                      (615, 521),  #用户登录 0
                      (749, 453),  #确认 1
                      (1060, 97),  #关闭弹窗 2
                      (1024, 12),  #数据按钮 3
                      (1090, 222),   #下载历史数据 4
                      (432, 253),  #勾选日线 5
                      (826, 551),  #点击下载 6
                      (952, 165),  #关闭日线下载窗口 7

                      (1024, 12),  # 数据按钮 8
                      (1088, 247),  # 下载财务数据 9
                      (661, 514),  #下载财务数据左边 10
                      (953, 515),  #下载财务数据右边 11
                      (988, 160),  #关闭财务数据窗口 12



                      (1352, 12),  #关闭主窗口 13
                      (576, 525)   #确认退出 14
                  ]}

        subprocess.Popen(r'C:\new_jyplug\tdxw.exe')  # hp
        sleep(3)
        pyautogui.click(tdxpt[cc][0],button='left') #免费
        # sleep(0.25)
        # pyautogui.click(tdxpt[cc][1]) #确定
        sleep(8)
        ##关闭弹窗
        pyautogui.click(tdxpt[cc][2])
        sleep(0.25)
        # 数据
        pyautogui.click(tdxpt[cc][3])
        sleep(0.25)
        # 数据下载
        pyautogui.click(tdxpt[cc][4])
        sleep(0.25)
        # 选择日期范围
        pyautogui.click(tdxpt[cc][5])
        sleep(0.25)
        # 点击下载
        pyautogui.click(tdxpt[cc][6])
        sleep(60)
        # 关闭下载日线数据窗口
        pyautogui.click(tdxpt[cc][7])



        # # 数据下载
        # pyautogui.click(tdxpt[cc][8])
        # sleep(0.25)
        # # 财务数据
        # pyautogui.click(tdxpt[cc][9])
        # sleep(0.25)
        # # 点击下载左边
        # pyautogui.click(tdxpt[cc][10])
        #
        # # 下载右边
        # pyautogui.click(tdxpt[cc][11])
        #
        # sleep(60)
        # # 关闭财务下载日线数据窗口
        # pyautogui.click(tdxpt[cc][12])

        sleep(0.25)
        # 退出
        pyautogui.click(tdxpt[cc][13])
        sleep(0.25)
        # 确认退出
        pyautogui.click(tdxpt[cc][14])
        print("---------------------------通达信自动下载  结束-------------------------------")
