from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vector import *

FS_VECTOR = Vector(1, 0) + Vector(1, -60) + Vector(1, -180) + Vector(1, -120) + Vector(2, 0) + Vector(1, 60)


class Line:
    def __init__(self, vector: Vector, variant: bool):
        self.vector = vector
        self.variant = variant

    def flowsnake(self) -> list:
        out = []
        d = self.vector.distance / FS_VECTOR.distance
        a = (self.vector.angle - FS_VECTOR.angle) % 360
        if self.variant:
            out.append(Line(Vector(d, a), True))
            a -= 60
            out.append(Line(Vector(d, a), False))
            a -= 120
            out.append(Line(Vector(d, a), False))
            a += 60
            out.append(Line(Vector(d, a), self.variant))
            a += 120
            out.append(Line(Vector(d, a), True))
            out.append(Line(Vector(d, a), True))
            a += 60
            out.append(Line(Vector(d, a), False))
        else:
            a += 60
            out.append(Line(Vector(d, a), True))
            a -= 60
            out.append(Line(Vector(d, a), False))
            out.append(Line(Vector(d, a), False))
            a -= 120
            out.append(Line(Vector(d, a), self.variant))
            a -= 60
            out.append(Line(Vector(d, a), True))
            a += 120
            out.append(Line(Vector(d, a), True))
            a += 60
            out.append(Line(Vector(d, a), False))
        return out


class FlowSnake(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flow Snake - Iteration 0")
        self.setFixedSize(650, 650)

        self.iterations = [[Line(Vector(480, FS_VECTOR.angle + 90), True)]]
        self.current_iteration = 0

        self.points = []
        self.prepare_drawing()
        for i in range(4):
            self.next()

        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Right:
            self.next()
        elif e.key() == Qt.Key_Left:
            self.prev()

    def prev(self):
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.setWindowTitle(f"Flow Snake - Iteration {self.current_iteration}")
            self.repaint()

    def next(self):
        if self.current_iteration < 7:
            self.current_iteration += 1
            if len(self.iterations) <= self.current_iteration:
                self.iterations.append(self.flowsnake(self.iterations[-1]))
                self.prepare_drawing()
            self.setWindowTitle(f"Flow Snake - Iteration {self.current_iteration}")
            self.repaint()

    @staticmethod
    def flowsnake(fs: List[Line]) -> List[Line]:
        out = []
        for line in fs:
            out += line.flowsnake()
        return out

    def prepare_drawing(self):
        lines = self.iterations[self.current_iteration]
        p = Point(0, 0)
        minx, miny = maxx, maxy = p
        points = [p]
        for line in lines:
            p += line.vector.to_point()
            minx = min(p.x, minx)
            miny = min(p.y, miny)
            maxx = max(p.x, maxx)
            maxy = max(p.y, maxy)
            points.append(p)

        midpoint = Point((maxx + minx) / 2, (maxy + miny) / 2)
        midpoint = Point(self.width() / 2, self.height() / 2) - midpoint
        self.points.append([p + midpoint for p in points])

    def paintEvent(self, e: QPaintEvent):
        qp = QPainter(self)
        col = QColor("#111111")
        qp.setPen(col)
        qp.setBrush(col)
        qp.drawRect(self.rect())

        colors = [
            0xff0000,
            0xffff00,
            0x008800,
            0x00ffff,
            0x0000ff,
        ]

        points = self.points[self.current_iteration]
        lines = len(points) - 1
        for i, (p1, p2) in enumerate(zip(points[:-1], points[1:])):
            p = i / lines
            c = p * (len(colors) - 1)
            color = int(c)
            p = c - int(c)
            color1 = [colors[color] >> j & 0xff for j in range(16, -1, -8)]
            color2 = [colors[color + 1] >> j & 0xff for j in range(16, -1, -8)]

            qp.setPen(QPen(QColor(
                round(color1[0] * (1 - p) + color2[0] * p),
                round(color1[1] * (1 - p) + color2[1] * p),
                round(color1[2] * (1 - p) + color2[2] * p)
            ), 1))

            qp.drawLine(*p1, *p2)


if __name__ == '__main__':
    app = QApplication([])
    flowsnake = FlowSnake()
    app.exec_()
