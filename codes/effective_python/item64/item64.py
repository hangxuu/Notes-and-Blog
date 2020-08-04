import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

NUMBERS = [ (1963309, 2265973), (2030677, 3814172), (1551645, 2229620),
            (2039045, 2020802), (1823712, 1924928), (2293129, 1020491),
            (1281238, 2273782), (3823812, 4237281), (3812741, 4729139),
            (1292391, 2123811),
] * 10


# 暴力GCD
def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


def main():
    start = time.time()
    results = list(map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"Token {delta:.3f} seconds")


def main_thread():
    start = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"Thread token {delta:.3f} seconds")


def main_process():
    start = time.time()
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"Processing token {delta:.3f} seconds")


if __name__ == "__main__":
    main()
    main_thread()
    main_process()

