from astropy.io import ascii

class FixedWidthSuite:
    def setup(self):
        self.table = ascii.read('benchmarks/files/fixedwidth.txt', format='fixed_width')
    def time_read(self):
        ascii.read('benchmarks/files/fixedwidth.txt', format='fixed_width')
    def time_write(self):
        ascii.write(self.table, 'output.txt', Writer=ascii.FixedWidth)
