import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vector import Point, Vector


class Circles(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Circles")
        self.setFixedSize(640, 480)

        self.timer = QBasicTimer()
        self.timer.start(20, self)

        self.angle = 0
        self.last_point = None

        self.img = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.ip = QPainter(self.img)

        self.show()

    def timerEvent(self, e: QTimerEvent):
        if e.timerId() == self.timer.timerId():
            self.angle += 17
            self.repaint()

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()

    def paintEvent(self, _: QPaintEvent):
        qp = QPainter(self)

        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())

        qp.drawImage(0, 0, self.img)

        center = Point(self.width() / 2, self.height() / 2)
        length = random.randint(100, 200)
        end = center + Vector(length, self.angle).to_point()
        qp.setPen(QPen(Qt.black, 2))
        qp.drawLine(*center, *end)

        self.ip.setPen(QPen(Qt.black, 2))
        self.ip.drawPoint(*end)

        if self.last_point:
            self.ip.drawLine(*self.last_point, *end)
        self.last_point = end


if __name__ == '__main__':
    app = QApplication([])
    circles = Circles()
    app.exec_()
