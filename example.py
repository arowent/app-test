import string

def get_dictionary(value):
    if value <= len(string.ascii_lowercase):
        return dict(enumerate(string.ascii_lowercase[:value], 1))
    else:
        return f'Введите допустимое значение, меньше или равное {len(string.ascii_lowercase)}'


if __name__ == '__main__':
    print(list(reversed('hello')))
    print(get_dictionary(12))