from queue import Queue
from threading import Thread
import time
# 缓冲区大小为10，当my_queue.qsize() == 10时，阻塞put方法
my_queue = Queue(10)


def consumer():
    i = 0
    while True:
        my_queue.get()
        print(f"Consuming item {i}.")
        my_queue.task_done()    # 对每一个item调用task_done()
        i += 1
        if i == 100:
            break


def producer():
    i = 0
    while True:
        print(f"Producing item {i}")
        my_queue.put(i)
        i += 1
        if i == 100:
            # 假设只生产100个元素，则 i == 100时任务完成
            print('Producer done')
            break


thread_consumer = Thread(target=consumer)
thread_consumer.start()
thread_producer = Thread(target=producer)
thread_producer.start()


my_queue.join()    # 只有所有item都调用了task_done()，join才会解除阻塞。也就是说，一旦my_queue.join()执行，任务就一定完成了。下面两句甚至是多余的。
# thread_consumer.join()
# thread_producer.join()
time.sleep(1)
print(f"my_queue size: {my_queue.qsize()}")
