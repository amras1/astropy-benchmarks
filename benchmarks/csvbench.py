from astropy.io import ascii

class CSVSuite:
    def setup(self):
        self.table = ascii.read('benchmarks/files/csv.csv', format='csv')
    def time_read(self):
        ascii.read('benchmarks/files/csv.csv', format='csv')
    def time_write(self):
        ascii.write(self.table, 'output.csv', Writer=ascii.Csv)
