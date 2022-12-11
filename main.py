
# Разработка программа защиты от несанкционированного копирования со съемных носителей

from UsbWidget import *
from UsbListener import *
from resoursePath import *

import sys, wmi

from PyQt5.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QGraphicsOpacityEffect, QFrame
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase

class BorderlessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.center()
        self.setFixedSize(330, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPos = self.pos()

        self.centralWidget = QLabel(self)
        self.centralWidget.setPixmap(QPixmap(resource_path("mainframe.png")))

        QFontDatabase.addApplicationFont(".\\Resourses\\font\\static\\JosefinSlab-SemiBold.ttf")
        QFontDatabase.addApplicationFont(".\\Resourses\\font\\static\\JosefinSlab-Light.ttf")
        self.nameLabel = QLabel("COPYSTOP", self)
        self.nameLabel.setFont(QFont("Josefin Slab", 28))
        self.nameLabel.setStyleSheet("color: white")
        self.nameLabel.move(7, 7)

        buttonStyleSheet = ("""
            QPushButton::hover {
                color : #ff5252;
            }
            QPushButton {
                border: none;
                color: white;
            }
            """)

        self.hideButton = QPushButton("_", self)
        self.hideButton.setFont(QFont("Josefin Slab", 27))
        self.hideButton.move(250, 0)
        self.hideButton.setStyleSheet(buttonStyleSheet)
        self.hideButton.clicked.connect(self.showMinimized)

        self.exitButton = QPushButton("X", self)
        self.exitButton.setFont(QFont("Josefin Slab", 27))
        self.exitButton.move(290, 11)
        self.exitButton.setStyleSheet(buttonStyleSheet)
        self.exitButton.clicked.connect(sys.exit)

        self.contentBox = QLabel(self)
        self.contentBox.setPixmap(QPixmap(resource_path("content_box.png")))
        self.contentBox.move(15, 67)

        self.usbName = QLabel("USB NAME")
        self.usbName.setFont(QFont("Josefin Slab", 15))
        self.usbName.setStyleSheet("color: #433633")

        self.usbStatus = QLabel("STATUS")
        self.usbStatus.setFont(QFont("Josefin Slab", 15))
        self.usbStatus.setStyleSheet("color: #433633")

        self.titleWidget = QWidget()
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.usbName)
        self.titleLayout.addStretch(1)
        self.titleLayout.addWidget(self.usbStatus)
        self.titleLayout.addStretch(1)
        self.titleLayout.setContentsMargins(50, 0, 0, 0)
        self.titleWidget.setLayout(self.titleLayout)
        self.titleWidget.setMinimumHeight(35)


        self.usbList = QVBoxLayout()
        for usbDrive in wmi.WMI().Win32_LogicalDisk(DriveType = 2):
            self.usbList.addWidget(UsbWidget(usbDrive.VolumeName + " (" + usbDrive.name + ")"))
        self.usbList.addStretch()

        self.setUsbListener()

        self.usbContainer = QWidget()
        self.usbContainer.setLayout(self.usbList)
        self.usbContainer.setObjectName("usbContainerLink")
        self.setStyleSheet("""
            QWidget#usbContainerLink {
                background-color: #f7f0f5;
            }
        """)
        self.usbContainer.setStyleSheet("")

        self.usbScrollArea = QScrollArea()
        self.usbScrollArea.setFrameShape(QFrame.NoFrame)
        self.usbScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.usbScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.usbScrollArea.setWidgetResizable(True)
        self.usbScrollArea.setMinimumHeight(210)
        self.usbScrollArea.setMaximumHeight(210)
        self.usbScrollArea.setStyleSheet('''
            QScrollBar:vertical {
                border: none;
                background: #5c5552;
                width: 6px;
                border-radius: 0px;
                background:none;
            }

            QScrollBar::handle:vertical {	
                background-color: rgb(143, 133, 125);
                border-radius: 2px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover{	
                background-color: #EF2D56;
            }
            QScrollBar::handle:vertical:pressed {	
                background-color: rgb(125, 46, 52);
            }

            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-line:vertical {
                height: 0px;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            ''')
        self.usbScrollArea.setWidget(self.usbContainer)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.addWidget(self.titleWidget)
        self.contentLayout.addWidget(self.usbScrollArea)
        self.contentLayout.addStretch()
        self.contentBox.setLayout(self.contentLayout)

        self.infoButton = QPushButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("info_icon.png")), QIcon.Normal, QIcon.Off)
        self.infoButton.setIcon(icon)
        self.infoButton.setIconSize(QSize(35, 35))
        self.infoButton.setStyleSheet("border: none;")
        self.infoButton.move(30, 355)
        self.infoButton.clicked.connect(lambda: self.showInfo())

        self.infoBox = QLabel(self)
        self.infoBox.move(0, 67)
        self.infoBox.setPixmap(QPixmap(resource_path("info_box.png")))
        
        self.infoLayout = QVBoxLayout()
        self.infoHeader = QLabel("Information")
        self.infoHeader.setFont(QFont("Josefin Slab", 20))
        self.infoHeader.setStyleSheet("color: white")

        self.infoText = QLabel("This is a simple PyQt5 Application, which allows user to prevent unauthorized copying from USB drives.")
        self.infoText.setFont(QFont("Josefin Slab", 13))
        self.infoText.setStyleSheet("color: white")
        self.infoText.setWordWrap(True)
        self.infoText.setContentsMargins(20, 0, 0, 0)

        self.madeBy = QLabel("Made by >seeker_   ")
        self.madeBy.setFont(QFont("Josefin Slab", 13))
        self.madeBy.setStyleSheet("color: white")
        
        self.infoLayout.addWidget(self.infoHeader, 0, Qt.AlignCenter)
        self.infoLayout.addWidget(self.infoText)
        self.infoLayout.addStretch(2)
        self.infoLayout.addWidget(self.madeBy, 0, Qt.AlignRight)
        self.infoLayout.addStretch(1)
        self.infoBox.setLayout(self.infoLayout)

        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.0)
        self.infoBox.setGraphicsEffect(opacity)
        self.infoBoxStatus = False
        self.infoBox.hide()

        self.version = QLabel("VERSION: 1.0", self)
        self.version.setFont(QFont("Josefin Slab", 19))
        self.version.setStyleSheet("color: white")
        self.version.move(160, 357)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def showInfo(self):
        if self.infoBoxStatus == True:
            self.fade(self.infoBox)
            self.infoBoxStatus = False
        else:
            self.infoBox.show()
            self.unfade(self.infoBox)
            self.infoBoxStatus = True

    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self.animation.finished.connect(self.infoBox.hide)
        self.infoBoxStatus = False

    def unfade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def setUsbListener(self):
        self.thread = QThread()
        self.UsbListenerWorker = UsbListener()
        self.UsbListenerWorker.moveToThread(self.thread)

        self.thread.started.connect(self.UsbListenerWorker.run)
        self.UsbListenerWorker.receivedName.connect(self.addNewUsb)
        self.UsbListenerWorker.removedName.connect(self.removeUsb)

        self.thread.start()
    
    def addNewUsb(self, usbName):
        tempUsb = UsbWidget(usbName)

        # opacity = QGraphicsOpacityEffect()
        # opacity.setOpacity(0.0)
        # tempUsb.setGraphicsEffect(opacity)

        self.usbList.insertWidget(0, tempUsb)
        # self.unfade(tempUsb)
    
    def removeUsb(self, usbName):
        index = self.usbList.count() - 1
        while index >= 0:
            myWidget = self.usbList.itemAt(index).widget()
            if myWidget != None:
                if myWidget.objectName() == usbName:
                    self.usbList.removeWidget(myWidget)
            index -= 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BorderlessWindow()
    sys.exit(app.exec_())