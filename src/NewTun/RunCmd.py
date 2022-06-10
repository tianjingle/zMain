import os.path
import sys
import time
curPath=os.path.abspath(os.path.dirname(__file__))
rootPath=os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append("path")
import win32api


class RunCmd:

    shutdown="C:\\zMain-web\\shutdown.bat"

    run="C:\\zMain-web\\run.bat"

    #重启我们的java进程
    def execute(self):
        #wMain存在的话就重启一下
        if os.path.exists(self.shutdown) and os.path.exists(self.run):
            win32api.ShellExecute(0, 'open', self.shutdown, '', '', 1)
            print("start\t"+self.shutdown)
            time.sleep(5)
            win32api.ShellExecute(0, 'open', self.run, '', '', 1)
            print("start\t"+self.run)



# RunCmd().execute()
# print("123")