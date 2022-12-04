
from AnimatedToggle import *

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize

class USBWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.centerWidget = QWidget(self)
        self.centerWidget.setObjectName("usbWidget")

        self.usbIcon = QLabel()
        self.usbIcon.setPixmap(QPixmap(".\\Resourses/usb_unlocked.png"))

        self.usbName = QLabel("Name_Of_Usb")
        self.usbName.setFont(QFont("Josefin Slab", 15))
        self.usbName.setStyleSheet("color: white; outline: 2px #433633")
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor('#433633'))
        self.usbName.setGraphicsEffect(shadow)

        self.switch = AnimatedToggle()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 0, 0)
        self.layout.addWidget(self.usbIcon)
        self.layout.addWidget(self.usbName)
        self.layout.addStretch(1)
        self.layout.addWidget(self.switch)

        self.centerWidget.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget#usbWidget {
                background: QLinearGradient(x1: 0, y1: 0,
                                            x2: 1, y2: 0, 
                                            stop: 0 #D44D61, 
                                            stop: 1 #F7F0F5 );
            }
        """)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

    def setUsbName(self, name):
        self.usbName.setText(name)