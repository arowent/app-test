class AnimalName:
    def __init__(self) -> None:
        self._planet = 'Марс'
    _planet = 'Земля'


class Animal(AnimalName):
    """Класс для отображения свойств животного"""
    def __init__(self, name='Zebra', age=24) -> None:
        super.__init__(_planet)
        self.name = name

    def get_info(self):
        return self._planet


animal_one = Animal()
# animal_one._planet = 'Марс'
# print(animal_one.get_info())
print('Животное {} находится на планете {}'.format(
    animal_one.name,
    animal_one._planet
))
# print(Animal.__dict__)