import random
import math
import itertools


def get_result(passersby):
    if len(passersby) % 2 == 0:
        men = 0

        for i in range(len(passersby) // 2):
            max_number = max(passersby)
            men += max_number
            passersby.remove(max_number)

        return men - sum(passersby)
    else:
        print(sum(i for i in passersby if i % 2 == 0))
        return max(passersby) - min(passersby)


    # На 6 пройденных тестов
    # if len(passersby) % 2 == 0:
    #     max_number = max(passersby)
    #     passersby.remove(max_number)
    #     second_number = max(passersby)
        # passersby.remove(second_number)
    #     sum_pos = max_number + second_number
    #     print(sum_pos - sum(passersby))
    #     return sum_pos - sum(passersby)
    # else:
    #     return max(passersby) - min(passersby)


get_result([3, 10, 4, 8])
get_result([5, 12, 6])
# assert get_result([3, 10, 4, 8]) == 11
# assert get_result([5, 12, 6]) == 7
