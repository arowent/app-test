import numpy as np


class Point(object):
    __instance = None

    def __call__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def fullname(self):
        return 'Hello, {} {}!'.format(self.name, self.lastname)


pt = Point('Aloha', 'Lopatko')
pt2 = Point('Arowent', 'Lopatko')

print(pt.fullname())
print(pt2.fullname())
