<!-- GFM-TOC -->
* [一、多进程](#多进程)
    * [什么时候用多进程](#什么时候用多进程)
    * [多进程怎么用](#多进程怎么用)
* [二、多线程](#多线程)
    * [什么时候用多线程](#什么时候用多线程)
    * [多线程怎么用](#多线程怎么用)
* [三、协程](#协程)
    * [什么时候用协程](#什么时候用协程)
    * [协程怎么用](#协程怎么用)
* [四、多线程及协程的一些示例代码](#多线程及协程的一些示例代码)
* [参考资料](#参考资料)

<!-- GFM-TOC -->

## 多进程
进程是操作系统资源分配的基本单位。
### 什么时候用多进程
当需要真正的并行计算时，使用多进程能同时使用多个CPU核心。因此多进程特别适合CPU密集型应用。
### 多进程怎么用
对于高度并行的任务（各个任务之间没有依赖，不用交流，结果也是独立的），``concurrent.futures``的``ProcessPoolExecutor``类是第一选择。使用也很简单。示例：
```python
from concurrent import futures

def sha(size):
    # 计算型函数
    ...
    
SIZE = 3 # sha函数的参数
JOBS = 12 # 任务数

...
with futures.ProcessPoolExecutor() as executor:
    to_do = (executor.submit(sha, SIZE) for i in range(JOBS))
    for future in futures.as_completed(to_do):
        res = future.result()
        print(res)
```
如果使用场景较复杂，例如需要在进程之间传递数据，那么可以使用更底层的``multiprocessing``模块来处理。

## 多线程
线程是CPU独立调度的基本单位。

### 什么时候用多线程
GIL：全局解释器锁。Cpython执行python程序分为两步：1，把源程序翻译成字节码；2，使用基于堆栈的解释器运行字节码（字节码解释器的状态必须在python程序运行时保持一致）。Cpython解释器本身就不是线程安全的。因此需要加锁。GIL是互斥锁，以防止Cpython受到抢占式多线程的影响。

Python标准库中的所有阻塞型 I/O 函数都会释放 GIL，允许其他线程运行。``time.sleep()``函数也会释放 GIL。因此，尽管有 GIL，Python 线程还是能在 I/O 密集型应用中发挥作用。因此python多线程特别适合I/O密集型应用。

### 多线程怎么用
同多进程，对于高度并行的任务，``concurrent.futures``的``ThreadPoolExecutor``类是第一选择。使用和``ProcessPoolExecutor``类似，如下例：
```python
from concurrent import futures
...
def download_many_thread(alnum, total):
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        to_do = []
        for i in range(1, total + 1):
            future = executor.submit(download_one_for_multi, (alnum, i))
            to_do.append(future)
        result = []
        for future in futures.as_completed(to_do):
            res = future.result()
            result.append(res)
    # 结果顺序与调用顺序不一致（乱序，谁先运行结束谁在前面）
    return result
```
可以看出``ThreadPoolExecutor``类在用法上和``ProcessPoolExecutor``类基本相同。``ThreadPoolExecutor``类需要传入``max_workers``参数指定线程池大小，这个根据需要可以开到很大。而``ProcessPoolExecutor``一般不需要这个参数，它会默认使用``os.cpu_count()``函数返回的CPU数量。

除了使用``executor.submit``和``futures.as_complete``组合，也可以直接使用``executor.map``完成上述功能。
```python
def download_many_thread(alnum, total):
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(download_one_for_multi, [(alnum, i) for i in range(1, total + 1)])
    # 结果顺序与调用顺序一致
    return results
```
使用``executor.submit``和``futures.as_complete``更灵活。因为``executor.submit``可以调用不同的可调用对象，``executor.map``只能处理同一个可调用对象。此外，传给``futures.as_complete``函数的期物（Future对象，可以理解为正在运行的函数）集合可以来自多个``Executor``实例，例如一些由``ThreadPoolExecutor``实例创建， 另一些由``ProcessPoolExecutor``实例创建。

如果需要结果顺序与调用顺序保持一致呢？也不是一定要用``executor.map``，``futures.as_completed``函数也可以解决这个问题：把期物存储在一个字典中，提交期物时把期物与相关的信息联系起来；这样，``as_completed`` 迭代器产出期物后，就可以使用那些信息。示例：
```python
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
```

如果使用场景较复杂，例如线程之间需要交流，或者会发生资源争用，需要用到锁或信号量。那么可以使用更底层的``threading``模块来处理。

## 协程
协程相比多线程有什么优点？为什么要使用协程？

线程是由操作系统调度的，属于抢夺式多任务。就拿生产者消费者的例子说明。操作系统公平地运行这两个线程。假如生产者生产了一半时间片用完，操作系统就会保存它的生产现场。然后去运行消费者线程，由于消费者现在没有东西消费，它就会一直空等待，白白浪费一个时间片。

而协程属于协作式多任务。由协程自己控制何时让出时间片。生产者协程生产完毕后让出时间片，并通知等待它的消费者，此时消费者得到时间片后直接消费。就不会有CPU算力的浪费。

### 什么时候用协程
和多线程的使用场景相同：适合IO密集型应用。并且把多线程里的阻塞IO改为异步IO。
### 协程怎么用
现在已经不推荐使用 ``yield from`` 实现协程了。应该使用 ``async/await``定义协程，以及使用``asyncio``包实现异步IO，处理并发。

生产者-消费者的协程版本：
```python
import asyncio

async def consumer(i):
    item = await producer(i)
    print(f"Consuming {item}")


async def producer(i):
    # 模拟生产者生产时间
    await asyncio.sleep(1)
    print(f"Producing {i}")
    return i


async def main():
    need, i = 10, 0
    while i < need:
        await consumer(i)
        i += 1
    print("Work done")

asyncio.run(main())

```
《fluent python》 里的一段话能帮大家通俗理解 ``asyncio`` 的使用方法：使用 asyncio 包时，我们编写的异步代码中包含由 asyncio 本身驱动的协程（即委派生成器），而生成器最终把职责委托给 asyncio 包或第三方库（如 aiohttp）中的协程。这种处理方式相当于架起了管道，让 asyncio 事件循环（通过我们编写的协程）驱动执行低层异步 I/O 操作的库函数。

上例就是由 ``asyncio`` 驱动 ``main`` 协程，然后协程里一直 ``await`` 到执行异步IO操作的库函数 ``asyncio.sleep(1)``，这个 ``sleep`` 函数模拟生产者的生产过程。当生产完成后，事件循环把响应发给等待结果的消费者。得到响应后，消费者消费掉生产者的东西（打印输出），事件循环又把相应发给 ``main``协程，``main``协程记录已生产元素的件数（``i += 1``），向前执行到下一个 ``await`` 处，然后让出时间片（把控制权还给主循环）。

## 多线程及协程的一些示例代码
一个网络下载程序的单线程，多线程以及协程版本。上文中的部分代码片段即来自这些脚本。
- 普通单线程版本 [download_normal.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_normal.py)
- 多线程版本 [download_thread.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_thread.py)
- 协程版本 [download_asyncio.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_asyncio.py).

《fluent python》中一个线程和协程对比的例子。
- 线程版本 [spinner_thread.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/spinner_thread.py)
- 协程版本 [spinner_asyncio.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/spinner_asyncio.py)

## 参考资料
- [也来谈谈协程](https://zhuanlan.zhihu.com/p/147608872)
- 《fluent python》 chapter 16 - 18
- 《Effective python 2nd》 chapter 7
