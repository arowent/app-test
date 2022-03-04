import random
import math
import itertools


def get_sum(x, y, symbol):
    print(f'Your numbers: {x}, {y}')
    if symbol == "+":
        print(f'Calculation of values: {x+y}')
        return x + y
    elif symbol == "-":
        return x - y
    elif symbol == "*":
        return x * y
    elif symbol == "//":
        return x // y


def get_result(numb, arith):
    numb.insert(0, 0)
    arith_set = [i for i in itertools.permutations(arith)]
    rows = []
    line = []

    for i in arith_set:
        rows.append([x for x in itertools.chain(*itertools.zip_longest(numb, i)) if x is not None])

    for row in rows:
        print(f'\nrow: {row}')
        count = 0
        for i in row:
            if isinstance(i, str):
                symbol_index = row.index(i)
                count = get_sum(row[symbol_index - 1], row[symbol_index + 1], i)
                print(f'count: {count}')
                row[row.index(i) + 1] = count
                row.remove(row[row.index(i) - 1])
                row.remove(row[row.index(i)])
                row = row
                print(f'row after changes: {row}')
        line.append(count)
        print(f'count: {count}')
    print(line)
    return 'Good'


get_result([3, 4], ["+", "-"])
# get_result([1, 4, 2], ["-", "+", "*"])
