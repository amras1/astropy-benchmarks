from astropy.io.ascii import sextractor
import random
import string

def randword():
    length = random.randint(4, 8)
    return [random.choice(string.uppercase) for i in range(length)]
    
class SExtractorSuite:
    def setup(self):
        self.header = sextractor.SExtractorHeader()
        self.lines = []
        i = 0
        while i < 100000:
            if i % 20 == 0 and i != 0:
                i += 4
            i += 1
            self.lines.append('# {} {}'.format(i, randword()))
        self.lines.append('Non-header line')

    def time_header(self):
        self.header.get_cols(self.lines)
