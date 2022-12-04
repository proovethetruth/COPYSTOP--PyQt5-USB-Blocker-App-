
from USBWidget import *
from resoursePath import *

import sys
from PyQt5.QtCore import Qt, QPoint, QSize, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QGraphicsOpacityEffect
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
        self.titleWidget.setMaximumHeight(50)


        self.usbList = QVBoxLayout()
        for i in range(1):
            self.usbList.addWidget(USBWidget())
        self.usbList.addStretch()

        self.usbContainer = QWidget()
        self.usbContainer.setLayout(self.usbList)

        self.usbScrollArea = QScrollArea()
        self.usbScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.usbScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.usbScrollArea.setWidgetResizable(True)
        self.usbScrollArea.setWidget(self.usbContainer)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.addWidget(self.titleWidget)
        self.contentLayout.addWidget(self.usbScrollArea)

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

        infoFile = open(resource_path("info.txt"), "r")
        self.infoText = QLabel(infoFile.readline())
        self.version = QLabel(infoFile.readline(), self)

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

        self.version.setFont(QFont("Josefin Slab", 20))
        self.version.setStyleSheet("color: white")
        self.version.move(150, 355)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BorderlessWindow()
    sys.exit(app.exec_())