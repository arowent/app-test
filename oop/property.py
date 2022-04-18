class Person:
    def __init__(self, name, old):
        self.__name = name
        self.__old = old

    @property
    def old(self):
        return self.__old

    @old.setter
    def old(self, old):
        self.__old = old



p = Person('Alexey', 24)
p.old = 25
print(p.old, p.__dict__)