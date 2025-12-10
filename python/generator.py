import random

def fuc1():
    while True:
        yield random.randrange(1,100)

generator=fuc1()

for _ in range(9):
    print(next(generator))