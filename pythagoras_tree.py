from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vector import *

ANGLE = 30


class Square:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        vector = (p2 - p1).to_vector()
        vector.angle -= 90
        self.p3 = p2 + vector.to_point()
        self.p4 = p1 + vector.to_point()

        self.triangle = None

    def __iter__(self):
        yield self.p1, self.p2, self.p3, self.p4
        if self.triangle:
            yield from self.triangle

    def iterate(self):
        if self.triangle is None:
            self.triangle = Triangle(self.p4, self.p3)
        else:
            self.triangle.iterate()


class Triangle:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        vector = (p2 - p1).to_vector()
        vector.angle -= ANGLE
        vector.distance *= math.cos(deg2rad(ANGLE))
        self.p3 = p1 + vector.to_point()

        self.square1 = self.square2 = None

    def __iter__(self):
        yield self.p1, self.p2, self.p3
        if self.square1 is not None:
            yield from self.square1
            yield from self.square2

    def iterate(self):
        if self.square1 is None:
            self.square1 = Square(self.p1, self.p3)
            self.square2 = Square(self.p3, self.p2)
        else:
            self.square1.iterate()
            self.square2.iterate()


class PyTree(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pythagoras Tree - Iteration 0")
        self.setFixedSize(900, 600)

        self.tree = Square(
            Point(self.width() / 2 - 50, self.height() - 20),
            Point(self.width() / 2 + 50, self.height() - 20)
        )
        self.iterations = [list(self.tree)]
        self.current_iteration = 0

        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Right:
            self.current_iteration += 1
            if len(self.iterations) <= self.current_iteration:
                self.tree.iterate()
                self.iterations.append(list(self.tree))
            self.setWindowTitle(f"Pythagoras Tree - Iteration {self.current_iteration}")
            self.repaint()
        elif e.key() == Qt.Key_Left:
            if self.current_iteration > 0:
                self.current_iteration -= 1
                self.setWindowTitle(f"Pythagoras Tree - Iteration {self.current_iteration}")
                self.repaint()

    def paintEvent(self, _: QPaintEvent):
        qp = QPainter(self)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())

        qp.setPen(Qt.black)

        for polygon in self.iterations[self.current_iteration]:
            qp.drawPolygon(*(QPoint(*p) for p in polygon))


if __name__ == '__main__':
    app = QApplication([])
    tree = PyTree()
    app.exec_()
