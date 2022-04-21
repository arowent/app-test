class Cat:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__}: {self.name}"

    def __str__(self) -> str:
        return f"{self.name}"


class Point:
    def __init__(self, *args) -> None:
        self.__coords = args

    def __len__(self):
        return len(self.__coords)

    def __abs__(self):
        return list(map(abs, self.__coords))

p = Point(1, -2)
print(len(p))
print(abs(p))


# c = Cat('Васька')
# print(c)
