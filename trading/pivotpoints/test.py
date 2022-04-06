import sys
import random

args = sys.argv
print(f'args: {args} | type: {type(args)}')

x = random.randrange(int(args[1]))
y = random.choice(['apple', 'banana', 'cherry', 'durian'])

print(x)