from collections import defaultdict

current = {'green': 12, 'blue': 3}
increments = [('red', 3),
              ('blue', 17),
              ('orange', 9)
              ]


# closure
def count_missing(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


result, count = count_missing(current, increments)
assert count == 2


# class with __call__
class CountMissing:
    def __init__(self):
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return 0


def count_missing_2(current, increments):
    counter = CountMissing()
    result = defaultdict(counter, current)
    for key, amount in increments:
        result[key] += amount

    return result, counter.count


_, count = count_missing_2(current, increments)
assert count == 2