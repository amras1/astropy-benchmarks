from astropy.io import ascii

class TabSeparatedSuite:
    def setup(self):
        self.table = ascii.read('benchmarks/files/tab.txt', format='tab')
    def time_read(self):
        ascii.read('benchmarks/files/tab.txt', format='tab')
    def time_write(self):
        ascii.write(self.table, 'output.txt', Writer=ascii.Tab)
