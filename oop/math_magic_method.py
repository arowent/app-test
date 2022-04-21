"""
__add__() - для операций сложения
__sub__() - для операций вычитания
__mul__() - для операций умножения
__truediv__() - для операций деления
"""


class Clock:
    __DAY = 86400

    def __init__(self, seconds: int) -> None:
        if not isinstance(seconds, int):
            raise TypeError("Секунды должны быть целым числом")
        self.seconds = seconds % self.__DAY

    def get_time(self):
        s = self.seconds % 60
        m = (self.seconds // 60) % 60
        h = (self.seconds // 3600) % 24
        return f"{self.__getformatted(h)}:{self.__getformatted(m)}:{self.__getformatted(s)}"

    @classmethod
    def __getformatted(cls, x):
        return str(x).rjust(2, "0")

    def __add__(self, other):
        if not isinstance(other,(int, Clock)):
            raise ArithmeticError("Правый операнд должен быть int или Clock")
        sc = other
        if isinstance(other, Clock):
            sc = other.seconds
        return Clock(self.seconds + sc)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        if not isinstance(other, (int, Clock)):
            raise ArithmeticError("Правый операнд должен быть int или Clock")

        sc = other
        if isinstance(other, Clock):
            sc = other.seconds
        self.seconds += sc
        return self


c1 = Clock(1000)
c2 = Clock(2000)
c3 = c1 + c2
print(c3.get_time())
