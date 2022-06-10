import sys
import os
curPath=os.path.abspath(os.path.dirname(__file__))
rootPath=os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\myzMain\\venv\\Lib\\site-packages")
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\myzMain\\venv\\Lib\\site-packages\\win32")
from src.NewTun.zMain import zMain



zMain()