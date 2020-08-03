"""
author: hangxuu@qq.com

"""

import requests
import os
import time

BASE_DIR = r'C:\Downloads\test'
BASE_URL = f'https://www.example.com'


def save_fig(image, filename):
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(image)
        print(f"{filename} downloaded!")


def get_image(alnum, num):
    url = f'{BASE_URL}{alnum}/{num}.jpg'
    resp = requests.get(url)
    return resp.content


def download_one(alnum, num):
    filename = f'{alnum}_{num}.jpg'
    image = get_image(alnum, num)
    save_fig(image, filename)
    return filename


def download_many(alnum, total):
    results = []
    for i in range(1, total + 1):
        filename = download_one(alnum, i)
        results.append(filename)
    return results


if __name__ == "__main__":
    alnum = '13052'
    num = 64
    start = time.time()
    res = download_many(alnum, num)
    print(list(res))
    end = time.time()
    print(f"Total use {end - start:.2f} seconds")