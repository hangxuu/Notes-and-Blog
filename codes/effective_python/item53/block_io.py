import select
import socket
import time
from threading import Thread


def slow_systemcall():
	select.select([socket.socket()], [], [], 0.1)

start = time.time()
for _ in range(5):
	slow_systemcall()

end = time.time()
delta = end - start
print(f'Seq took {delta:.3f} seconds')

start = time.time()
threads = []
for _ in range(5):
	thread = Thread(target=slow_systemcall)
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()

end = time.time()
delta = end - start
print(f'Threads took {delta:.3f} seconds')

