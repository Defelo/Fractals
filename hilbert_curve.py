from typing import List


def hilbert(h: List[tuple]) -> List[tuple]:
    return [((1 - y) / 2, 1 - x / 2) for x, y in h] + \
           [(x / 2, y / 2) for x, y in h] + \
           [(1 - (1 - x) / 2, y / 2) for x, y in h] + \
           [(1 - (1 - y) / 2, 1 - (1 - x) / 2) for x, y in h]


H = [(.5, .5)]
for i in range(3):
    print(H)
    H = hilbert(H)
