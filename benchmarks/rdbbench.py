from astropy.io import ascii

class RDBSuite:
    def setup(self):
        self.header = ascii.RdbHeader()
        f = open('benchmarks/files/rdb/string.txt')
        self.lines = f.read().split('\n')[2:]
        f.close()
    def time_get_cols(self):
        self.header.get_cols(self.lines)
