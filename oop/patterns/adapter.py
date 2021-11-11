# JSON - str
# XML - int

class Old(object):
    def get(self):
        return '1234'


class New:
    def get_int(self):
        return 456


class Adapter(New):
    def get(self):
        # return str(super(Adapter, self).get())
        return str(self.get_int())


def main(obj):
    print("Результат: " + obj.get())


if __name__ == '__main__':
    obj = Adapter()
    main(obj)