class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __checkValue(value):
        if isinstance(value, int) or isinstance(value, float):
            return True
        return False

    def setCoords(self, x, y):
        if Point.__checkValue(x) and Point.__checkValue(y):
            self.__x = x
            self.__y = y
        else:
            print('Неправильный тип данных')

    def getCoords(self):
        return self.__x, self.__y

pt = Point(1, 2)
print(pt.getCoords())
pt.setCoords(10, 20)
print(pt.getCoords())