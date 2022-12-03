import sys
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase, QIcon


class BorderlessWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.centralWidget = QLabel(self)
        self.centralWidget.setPixmap(QPixmap(".\\Resourses/mainframe.png"))

        self.center()
        self.setFixedSize(330, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.oldPos = self.pos()

        QFontDatabase.addApplicationFont(".\\Resourses\\font\\static\\JosefinSlab-SemiBold.ttf")
        self.nameLabel = QLabel("COPYSTOP", self)
        self.nameLabel.setFont(QFont("Josefin Slab", 30))
        self.nameLabel.setStyleSheet("color: white")
        self.nameLabel.move(5, 5)


        self.exitButton = QPushButton(self)
        self.exitButton.setStyleSheet("border: none;")
        exitIcon = QIcon()
        exitIcon.addPixmap(QPixmap(".\\Resourses/exit_icon.png"), QIcon.Normal, QIcon.Off)
        self.exitButton.setIcon(exitIcon)
        self.exitButton.setIconSize(QSize(60, 60))
        self.exitButton.move(270, 0)
        self.exitButton.clicked.connect(self.exit)

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

    def exit(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BorderlessWindow()
    sys.exit(app.exec_())