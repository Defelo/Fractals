from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vector import Point


class Koch(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Koch Curve - Iteration 0")
        self.setFixedSize(640, 480)

        self.iterations = [[Point(20, self.height() - 20), Point(self.width() - 20, self.height() - 20)]]
        self.current_iteration = 0

        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Right:
            if self.current_iteration < 7:
                self.current_iteration += 1
                if len(self.iterations) <= self.current_iteration:
                    self.iterations.append(self.koch(self.iterations[-1]))
                self.setWindowTitle(f"Koch Curve - Iteration {self.current_iteration}")
                self.repaint()
        elif e.key() == Qt.Key_Left:
            if self.current_iteration > 0:
                self.current_iteration -= 1
                self.setWindowTitle(f"Koch Curve - Iteration {self.current_iteration}")
                self.repaint()

    @staticmethod
    def koch(k: List[Point]) -> List[Point]:
        out = k[:1]
        for p1, p2 in zip(k[:-1], k[1:]):
            vector = (p2 - p1).to_vector()
            vector.distance /= 3
            out.append(out[-1] + vector.to_point())
            vector.angle -= 60
            out.append(out[-1] + vector.to_point())
            vector.angle += 120
            out.append(out[-1] + vector.to_point())
            out.append(p2)
        return out

    def paintEvent(self, e: QPaintEvent):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())

        qp.setPen(QPen(Qt.black, 1))

        curve = self.iterations[self.current_iteration]
        for p1, p2 in zip(curve[:-1], curve[1:]):
            qp.drawLine(p1.x, p1.y, p2.x, p2.y)


if __name__ == '__main__':
    app = QApplication([])
    koch = Koch()
    app.exec_()
