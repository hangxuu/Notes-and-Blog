"""
author: hangxuu@qq.com

"""

import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures


BASE_DIR = r'C:Downloads\test'
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


# 使用map需要注意，需写为单参数函数，传入元组，在函数中进行序列解包。
def download_one_for_multi(args):
    alnum, num = args
    filename = f'{alnum}_{num}.jpg'
    image = get_image(alnum, num)
    save_fig(image, filename)
    return filename


def download_many_thread(alnum, total):
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(download_one_for_multi, [(alnum, i) for i in range(1, total + 1)])
    # 结果顺序与调用顺序一致
    return results


# 更灵活的版本，使用 submit 和 as_completed 实现。
# 说它更灵活是因为 submit 可以调用不同的可调用对象，map 只能处理同一个可调用对象。
def download_many_thread2(alnum, total):
    with ThreadPoolExecutor(max_workers=20) as executor:
        to_do = []
        for i in range(1, total + 1):
            future = executor.submit(download_one_for_multi, (alnum, i))
            to_do.append(future)

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            results.append(res)
    # 结果顺序与调用顺序不一致（乱序，谁先运行结束谁在前面）
    return results


def download_many_thread3(alnum, total):
    with ThreadPoolExecutor(max_workers=20) as executor:
        # 使用字典而不是列表
        to_do_map = {}
        for i in range(1, total + 1):
            future = executor.submit(download_one_for_multi, (alnum, i))
            to_do_map[future] = i

        results = []
        for future in futures.as_completed(to_do_map):
            res = future.result()
            results.append((res, to_do_map[future]))
    # 根据字典保存的信息做排序即可（这里保存的就是生成期物的顺序）。
    results = [item[0] for item in sorted(results, key=lambda a:a[1])]
    return results


if __name__ == "__main__":
	# 示例多线程多参数传递
    alnum = '13052'
    num = 64
    start = time.time()
    # res = download_many_thread2(alnum, num)    # 版本1
    # res = download_many_thread2(alnum, num)    # 版本2
    res = download_many_thread3(alnum, num)    # 版本3
    print(list(res))
    end = time.time()
    print(f"Total use {end - start:.2f} seconds")
