import random
import math
import itertools


def get_result(numb, arith):
    numb.insert(0, 0)
    arith_set = [i for i in itertools.permutations(arith)]
    line = []
    numbers = []

    for i in arith_set:
        line.append([x for x in itertools.chain(*itertools.zip_longest(numb, i)) if x is not None])

    # print(line)
    for i in line:
        print(i)



    # for i in line:
    #     text = ''.join(map(str, i))
    #     print(f'text: {text}')
    #     for i in text:
    #         if i == "*":
    #             print('Yes')
    #     numbers.append(eval(text))
    #
    # print(f'numbers: {numbers}')
    # max_number = max(numbers)
    # print(f'max(numbers): {max_number}\n')
    return 'Good'


# get_result([3, 4], ["+", "-"])
get_result([1, 4, 2], ["-", "+", "*"])
# assert get_result([3, 4], ["+", "-"]) == 1
# assert get_result([1, 4, 2], ["-", "+", "*"]) == 6
