import heapq
from collections import deque
from itertools import chain
from collections import OrderedDict


def unpacking(sequence):
    username, email, *numbers = sequence
    return 'User \'{}\' with email - {} | numbers: {}'.format(username, email, numbers)


sequence_unpacking = unpacking(['arowent', 'arowent@mail.ru', '782', '510'])
# print(sequence_unpacking)

# 1.4. Search for N maximum and minimum elements
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

# print(heapq.nlargest(2, nums))  # limit max numbers
# print(heapq.nsmallest(2, nums))  # limit min numbers

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
# print(cheap)


# 1.5. Implementing a priority queue

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)


