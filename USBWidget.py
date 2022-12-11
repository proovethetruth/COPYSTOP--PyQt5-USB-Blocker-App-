
from AnimatedToggle import *
from UsbCrypt import UsbCrypt
from resoursePath import *

import stat

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize

class UsbWidget(QWidget):
    def __init__(self, inputName):
        super().__init__()
        self.setObjectName(inputName)
        self.centerWidget = QWidget(self)
        self.centerWidget.setObjectName("usbWidget")

        self.usbIcon = QLabel()
        self.usbIcon.setPixmap(QPixmap(resource_path("usb_unlocked.png")))

        self.usbName = QLabel(inputName)
        self.usbName.setFont(QFont("Josefin Slab", 15))
        self.usbName.setStyleSheet("color: white; outline: 2px #433633")
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor('#433633'))
        self.usbName.setGraphicsEffect(shadow)

        self.switch = AnimatedToggle()
        self.switch.stateChanged.connect(self.switchUsbAccess)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 0, 0)
        self.layout.addWidget(self.usbIcon, 0, Qt.AlignVCenter)
        self.layout.addWidget(self.usbName)
        self.layout.addStretch(1)
        self.layout.addWidget(self.switch)

        self.centerWidget.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget#usbWidget {

                border-radius: 10px;
                background: QLinearGradient(x1: 0, y1: 0,
                                            x2: 1, y2: 0, 
                                            stop: 0 #D44D61, 
                                            stop: 1 #F7F0F5 );
            }
        """)
        self.setMinimumWidth(150)
        self.setMinimumHeight(45)
        self.setMaximumHeight(45)

    def setUsbName(self, name):
        self.usbName.setText(name)

    def switchUsbAccess(self):
        path = self.objectName()[-3:-1] + "\\"
        UsbCrypt(path + "makima.jpg")
        

        # file = open(path + "makima.txt", "r")
        # print(file.read())
        # os.chmod(path, stat.S_IRUSR)
        # for root, dirs, _ in os.walk(path):
        #     for d in dirs:
        #         os.chmod(os.path.join(root, d), stat.S_IROTH)
        # #os.chmod(self.objectName()[-3:-1], stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)