from astropy.io import ascii

class RDBSuite:
    def setup(self):
        self.table = ascii.read('benchmarks/files/rdb.rdb', format='rdb')
    def time_read(self):
        ascii.read('benchmarks/files/rdb.rdb', format='rdb')
    def time_write(self):
        ascii.write(self.table, 'output.rdb', Writer=ascii.Rdb)
