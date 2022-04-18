class Tree:
    def __init__(self, kind, height):
        self.kind = kind
        self.height = height
        self.age = 0

    def info(self):
        return '{} years old {}. {} meters high.'.format(self.age, self.kind, self.height)

    def grow(self):
        self.age += 1
        self.height += 0.5


class FruitTree(Tree):
    def __init__(self, kind, height):
        super().__init__(kind, height)

    def give_fruits(self):
        flag: int = 50
        print(flag)
        return 'Collected 20kg of {}\'s, {} - {}'.format(self.kind, self.height, self.age)


tr1 = Tree('oak', 0.5)
print(tr1.info())
tr1.grow()
print(tr1.info())
ft1 = FruitTree('apple', 0.7)
print(ft1.give_fruits())
ft1.grow()
ft1.grow()
print(ft1.give_fruits())
