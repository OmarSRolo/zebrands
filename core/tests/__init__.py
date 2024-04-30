import time


class Benchmark:

    def __init__(self):
        self.start = 0
        self.elapsed = 0

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = (time.time() - self.start) * 1000
