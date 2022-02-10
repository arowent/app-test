import statistics


def get_result(ground):
    count = 0
    last_index = statistics.median_low(ground)
    # print(f'ground = {ground} and ground (modify) = {reverse}')
    while len(ground) != ground.count(last_index):
        for i in range(len(ground)):
            if ground[i] < last_index:
                ground[i] = ground[i] + 1
                count += 1
            elif ground[i] > last_index:
                ground[i] = ground[i] - 1
                count += 1
    print(ground)
    return count


assert get_result([1, 3, 2, 2]) == 2
assert get_result([6, 2, 8, 1]) == 11
print("Coding complete!")
