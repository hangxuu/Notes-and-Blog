import atexit
import gc
import io
import time
import collections
import os
import random
import string
from tempfile import TemporaryDirectory
from threading import Lock, Thread

random.seed(1234)


# Example 1
class NoNewData(Exception):
    pass


def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()


def tail_file(handle, interval, write_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            write_func(line)


def run_threads(handles, interval, output_path):
    with open(output_path, 'wb') as output:
        lock = Lock()

        def write(data):
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


def write_random_data(path, write_count, interval):
    with open(path, 'wb') as f:
        for i in range(write_count):
            time.sleep(random.random() * interval)
            letters = random.choices(
                string.ascii_lowercase, k=10)
            data = f'{path}-{i:02}-{"".join(letters)}\n'
            f.write(data.encode())
            f.flush()


def start_write_threads(directory, file_count):
    paths = []
    for i in range(file_count):
        path = os.path.join(directory, str(i))
        with open(path, 'w'):
            # Make sure the file at this path will exist when
            # the reading thread tries to poll it.
            pass
        paths.append(path)
        args = (path, 10, 0.1)
        thread = Thread(target=write_random_data, args=args)
        thread.start()
    return paths


def close_all(handles):
    time.sleep(1)
    for handle in handles:
        handle.close()


def setup():
    tmpdir = TemporaryDirectory()
    input_paths = start_write_threads(tmpdir.name, 5)

    handles = []
    for path in input_paths:
        handle = open(path, 'rb')
        handles.append(handle)

    Thread(target=close_all, args=(handles,)).start()

    output_path = os.path.join(tmpdir.name, 'merged')
    return tmpdir, input_paths, handles, output_path


# Example 5
def confirm_merge(input_paths, output_path):
    found = collections.defaultdict(list)
    with open(output_path, 'rb') as f:
        for line in f:
            for path in input_paths:
                if line.find(path.encode()) == 0:
                    found[path].append(line)

    expected = collections.defaultdict(list)
    for path in input_paths:
        with open(path, 'rb') as f:
            expected[path].extend(f.readlines())

    for key, expected_lines in expected.items():
        found_lines = found[key]
        assert expected_lines == found_lines, \
            f'{expected_lines!r} == {found_lines!r}'
        # print(f'{expected_lines!r} == {found_lines!r}')


tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()
