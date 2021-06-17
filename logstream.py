import mmap
import numpy as np

from itertools import cycle


class LogStream:
    def __init__(self, source_file: str, offsets=None, shuffle: bool = True):
        self.source_file = source_file
        if offsets:
            print("use given offsets")
        else:
            print("scan offsets")
            offsets = self.scan_offsets()
        self.offsets = offsets
        if shuffle:
            np.random.shuffle(self.offsets)
        # we want an inexhaustible source of offsets
        self.offsets = cycle(self.offsets)

    def __iter__(self):
        with open(self.source_file, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for position in self.offsets:
                mm.seek(position)
                record = mm.readline()
                yield record.decode().strip()

    def scan_offsets(self):
        tmp_offsets = []
        with open(self.source_file, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for _ in iter(mm.readline, b""):
                position = mm.tell()
                tmp_offsets.append(position)
        offsets = np.asarray(tmp_offsets, dtype="uint64")
        del tmp_offsets
        return offsets
