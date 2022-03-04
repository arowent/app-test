import statistics

def get_result(nums):
    med = statistics.median(nums)
    line = [x for x in nums if x < med]

    return line

if __name__ == '__main__':
    nums = [1, 3, 5, 6, 7]
    print(get_result(nums))
