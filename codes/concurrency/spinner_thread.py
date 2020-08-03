import threading
import itertools
import time


class Signal:
    go = True


def spin(msg, signal):
    for ch in itertools.cycle('|/-\\'):
        status = ch + ' ' + msg
        # \r:将光标回退到本行的开头位置
        print(status, flush=True, end='\r')
        time.sleep(.1)
        if not signal.go:
            print(' ' * len(status), end='\r')
            break


def slow_function():
    # 模拟IO
    time.sleep(3)
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("Thinking!", signal))
    print(f"Spinner object: {spinner}")
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
