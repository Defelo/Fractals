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

        self.angle1 = 0
        self.angle2 = 90
        self.last_point = None

        self.img = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.ip = QPainter(self.img)

        self.show()

    def timerEvent(self, e: QTimerEvent):
        if e.timerId() == self.timer.timerId():
            self.angle1 += 2
            self.angle2 += 7
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
        p1 = center + Vector(120, self.angle1).to_point()
        p2 = p1 + Vector(100, self.angle2).to_point()
        qp.setPen(QPen(Qt.black, 2))
        qp.drawLine(*center, *p1)
        qp.drawLine(*p1, *p2)

        self.ip.setPen(QPen(Qt.black, 2))
        self.ip.drawPoint(*p2)

        if self.last_point:
            self.ip.drawLine(*self.last_point, *p2)
        self.last_point = p2


if __name__ == '__main__':
    app = QApplication([])
    circles = Circles()
    app.exec_()
