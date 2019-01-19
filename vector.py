import math


def deg2rad(angle: float) -> float:
    return (angle % 360) / 180 * math.pi


def rad2deg(angle: float) -> float:
    return (angle * 180 / math.pi) % 360


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Point)
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Point(self.x / other, self.y / other)

    def to_vector(self):
        x, y = self.x, self.y
        if y == 0:
            return Vector(x, 90)
        distance = math.sqrt(x ** 2 + y ** 2)
        angle = rad2deg(math.atan(-x / y))
        if y > 0:
            distance *= -1
        return Vector(distance, angle)


class Vector:
    def __init__(self, distance: float, angle: float):
        if distance < 0:
            distance *= -1
            angle += 180
        self.distance = distance
        self.angle = angle % 360

    def __repr__(self) -> str:
        return f"Vector(distance={self.distance}, angle={self.angle})"

    def to_point(self):
        angle = self.angle % 360
        distance = self.distance
        if angle % 90 == 0:
            return [
                Point(0, -distance),
                Point(distance, 0),
                Point(0, distance),
                Point(-distance, 0)
            ][int(angle / 90)]

        if angle > 180:
            angle -= 180
            distance *= -1

        w = -1 / math.tan(deg2rad(angle))
        x = distance / math.sqrt(w ** 2 + 1)
        return Point(x, w * x)
