"""
author: hangxuu@qq.com

"""

import os
import time
import asyncio
import aiohttp

import atexit
import gc
import io


# Make sure Windows processes exit cleanly
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)


BASE_DIR = r'C:\Downloads\test'
BASE_URL = f'https://www.example.com'


def save_fig(image, filename):
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(image)
        print(f"{filename} downloaded!")


async def get_image_asy(alnum, num):
    url = f'{BASE_URL}{alnum}/{num}.jpg'
    async with aiohttp.request('GET', url) as resp:
        assert resp.status == 200
        image = await resp.read()
        return image


async def download_one_asy(alnum, num):
    image = await get_image_asy(alnum, num)
    save_fig(image, f'{alnum}_{num}.jpg')
    return num


async def download_many_asy(alnum, total):
    start = time.time()
    to_do = [download_one_asy(alnum, cc) for cc in range(1, total + 1)]
    await asyncio.gather(*to_do)
    end = time.time()
    print(f'Single thread uses {end - start} seconds')
    print('Job done')
    return total


if __name__ == "__main__":
    # 为了示例多参数传递（两个参数）
    alnum = '13052'
    num = 64
    asyncio.run(download_many_asy(alnum, num))
