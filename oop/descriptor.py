class Point3D:
    def __init__(self, x, y, z) -> None:
        self._x = x
        self._y = y
        self._z = z

    @classmethod
    def verify_coord(cls, coord):
        if type(coord) != int:
            raise TypeError("Координата должна быть целым числом")
