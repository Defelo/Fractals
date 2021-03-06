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

    def __iter__(self):
        yield self.x
        yield self.y

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
        if not self.x:
            return Vector(-self.y, 0)
        a = math.atan(self.y / self.x)
        d = self.x / math.cos(a)
        return Vector(d, rad2deg(a) + 90)


class Vector:
    def __init__(self, distance: float, angle: float):
        if distance < 0:
            distance *= -1
            angle += 180
        self.distance = distance
        self.angle = angle % 360

    def __repr__(self) -> str:
        return f"Vector(distance={self.distance}, angle={self.angle})"

    def __add__(self, other):
        assert isinstance(other, Vector)
        return (self.to_point() + other.to_point()).to_vector()

    def __sub__(self, other):
        assert isinstance(other, Vector)
        return (self.to_point() - other.to_point()).to_vector()

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Point(self.distance * other, self.angle)

    def __truediv__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Point(self.distance / other, self.angle)

    def to_point(self):
        return Point(
            math.cos(deg2rad(self.angle - 90)) * self.distance,
            math.sin(deg2rad(self.angle - 90)) * self.distance
        )
