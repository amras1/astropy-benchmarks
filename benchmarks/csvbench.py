from astropy.io import ascii

class CSVSuite:
    def setup(self):
        self.table = ascii.read('files/fieldingstats.csv', format='csv')
    def time_read(self):
        ascii.read('files/fieldingstats.csv', format='csv')
    def time_write(self):
        ascii.write(self.table, 'fieldingoutput.csv')
