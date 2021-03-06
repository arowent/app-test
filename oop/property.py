from string import ascii_letters


class Person:
    S_RUS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, fio, old, ps, weight) -> None:
        self.verify_fio(fio)
        self.verify_weight(weight)
        self.verify_ps(ps)

        self.__fio = fio.split()
        self.old = old
        self.__ps = ps
        self.__weight = weight

    @classmethod
    def verify_fio(cls, fio):
        if type(fio) != str:
            raise TypeError('ФИО должно быть строкой')
        f = fio.split()
        if len(f) != 3:
            raise TypeError('Неверный формат ФИО')

        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER
        for s in f:
            if len(s) < 1:
                raise TypeError("В ФИЛ должен быть хотя бы один символ")
            if len(s.strip(letters)) != 0:
                raise TypeError(
                    "В ФИО можно использовать только буквенные символы или дефис")

    @classmethod
    def verify_old(csl, old):
        if type(old) != int or old < 14 or old > 120:
            raise TypeError(
                "Возраст должен быть числом в диапазоне от 14 до 120")

    @classmethod
    def verify_weight(csl, weight):
        if type(weight) != float or weight < 20:
            raise TypeError(
                "Вес должен быть вещественным числом в диапазоне от 20 и выше")

    @classmethod
    def verify_ps(cls, ps):
        if type(ps) != str:
            raise TypeError("Паспорт должен быть строкой")
        s = ps.split()
        if len(s) != 2 or len(s[0]) != 4 or len(s[1]) != 6:
            raise TypeError("Неверный формат паспорта")
        for p in s:
            if not p.isdigit():
                raise TypeError("Серия и номер паспорта должны быть числами")

    @property
    def fio(self):
        return self.__fio

    @property
    def old(self):
        return self.__old

    @old.setter
    def old(self, old):
        self.verify_old(old)
        self.__old = old

    @property
    def passport(self):
        return self.__ps

    @old.setter
    def passport(self, ps):
        self.verify_ps(ps)
        self.__old = ps


p = Person('Лопатько Алексей Николаевич', 24, '1234 567890', 80.0)
p.passport = '8766 000000'
print(p.passport)
