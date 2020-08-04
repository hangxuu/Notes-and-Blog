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



### 什么时候用协程

### 协程怎么用



fluent python 里的一段话能帮大家通俗理解 ``asyncio`` 的使用方法：使用 asyncio 包时，我们编写的异步代码中包含由 asyncio 本身驱动的协程（即委派生成器），而生成器最终把职责委托给 asyncio 包或第三方库（如 aiohttp）中的协程。这种处理方式相当于架起了管道，让 asyncio 事件循环（通过我们编写的协程）驱动执行低层异步 I/O 操作的库函数。

## 多线程及协程的一些示例代码
一个网络下载程序的单线程，多线程以及协程版本。上文中的代码片段即来自这些脚本。
- 普通单线程版本 [download_normal.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_normal.py)
- 多线程版本 [download_thread.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_thread.py)
- 以及协程版本 [download_asyncio.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/download_asyncio.py).

fluent python 中一个线程和协程对比的例子
- 线程版本 [spinner_thread.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/spinner_thread.py)
- 协程版本 [spinner_asyncio.py](https://github.com/hangxuu/Notes-and-Blog/blob/master/codes/concurrency/spinner_asyncio.py)

## 参考资料
- [也来谈谈协程](https://zhuanlan.zhihu.com/p/147608872)