import sys
import requests
import base64

from memory_pic import a_png
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLCDNumber
from PyQt5.QtCore import QTimer
from PyQt5 import uic, QtGui

from ui import Ui_MainWindow

#设置运行图标
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('猫薄荷粉丝数监控')
        
        Logo = QtGui.QPixmap()
        Logo.loadFromData(base64.b64decode(a_png))
        icon = QtGui.QIcon()
        icon.addPixmap(Logo, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        self.label.setText('获取状态：准备中...')
        self.lcdNumber.display(0)
        self.pushButton.clicked.connect(self.UpdateNum)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateNum)
        self.timer.start(1000)
        
        self.show()
    
    def UpdateNum(self):
        num = self.GetFansNum()
        if num == -1:
            self.label.setText('获取状态：获取失败')
        else:
            self.label.setText('获取状态：获取成功')
        self.lcdNumber.display(num)
        
    def GetFansNum(self):
        """
        获取粉丝数
        40462777
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }
        url = 'https://api.bilibili.com/x/web-interface/card'
        params = {
            'mid': 40462777,
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                num = data['data']['follower']
                return num
            else: 
                return -1
        except:
            return -1

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())