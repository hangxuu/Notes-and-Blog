class InputData:
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super(PathInputData, self).__init__()
        self.path = path

    # read是实例方法多态
    def read(self):
        with open(self.path) as f:
            return f.read()


class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCounterWorker(Worker):

    # 实例方法多态
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


import os


def generate_input(data_dir):
    for name in os.listdir(data_dir):
        # 写死了
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        # 写死了
        workers.append(LineCounterWorker(input_data))

    return workers


from threading import Thread


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir):
    inputs = generate_input(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


import random


def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))


tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f"There are {result} lines.")


# 类方法多态
class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData2(GenericInputData):
    def __init__(self, path):
        super(PathInputData2, self).__init__()
        self.path = path

    # read是实例方法多态
    def read(self):
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        # 类方法多态
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCounterWorker2(GenericWorker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def mapreduce2(worker_class, input_class, config):
    # 类方法多态
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


config = {'data_dir': tmpdir}
result = mapreduce2(LineCounterWorker2, PathInputData2, config)
print(f"There are {result} lines.")
