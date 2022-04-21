import math

class Counter:
    def __init__(self) -> None:
        self.__counter = 0

    def __call__(self, step = 1, *args, **kwdsy):
        print("__call__")
        self.__counter += step
        return self.__counter

class StripChars:
    def __init__(self, chars):
        self.__counter = 0
        self.__chars = chars

    def __call__(self, *args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError("Аргемент должен быть строкой")

        return args[0].strip(self.__chars)

class Derivate:
    def __init__(self, func):
        self.__fn = func

    def __call__(self, x, dx=0.0001, *args, **kwargs):
        return (self.__fn(x + dx) - self.__fn(x)) / dx


# c = Counter()
# c()
# sc = StripChars("?:!.; ")
# res = sc("  Hello World  ")
# print(res)

@Derivate
def df_sin(x):
    return math.sin(x)




# df_sin = Derivate(df_sin)

print(df_sin(math.pi/4))