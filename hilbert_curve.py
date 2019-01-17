from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Hilbert(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hilbert Curve - Iteration 0")
        self.setFixedSize(480, 480)

        self.iterations = [self.hilbert([(.5, .5)])]
        self.current_iteration = 0

        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Right:
            if self.current_iteration < 7:
                self.current_iteration += 1
                if len(self.iterations) <= self.current_iteration:
                    self.iterations.append(self.hilbert(self.iterations[-1]))
                self.setWindowTitle(f"Hilbert Curve - Iteration {self.current_iteration}")
                self.repaint()
        elif e.key() == Qt.Key_Left:
            if self.current_iteration > 0:
                self.current_iteration -= 1
                self.setWindowTitle(f"Hilbert Curve - Iteration {self.current_iteration}")
                self.repaint()

    def paintEvent(self, _: QPaintEvent):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())

        qp.setPen(QPen(Qt.black, 1))

        curve = self.iterations[self.current_iteration]
        for (x1, y1), (x2, y2) in zip(curve[:-1], curve[1:]):
            qp.drawLine(x1 * self.width(), y1 * self.height(), x2 * self.width(), y2 * self.height())

    @staticmethod
    def hilbert(h: List[tuple]) -> List[tuple]:
        return [((1 - y) / 2, 1 - x / 2) for x, y in h] + \
               [(x / 2, y / 2) for x, y in h] + \
               [(1 - (1 - x) / 2, y / 2) for x, y in h] + \
               [(1 - (1 - y) / 2, 1 - (1 - x) / 2) for x, y in h]


if __name__ == '__main__':
    app = QApplication([])
    hilbert = Hilbert()
    app.exec_()
