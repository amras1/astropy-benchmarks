from astropy.table import Column
import random
import string

class TableSuite:
    def setup(self):
        lst = []
        lst.append([random.randint(-500, 500) for i in range(1000)])
        lst.append([random.random() * 500 - 500 for i in range(1000)])
        lst.append([''.join([random.choice(string.uppercase) for j in
                            range(6)]) for i in range(1000)])
        self.cols = [Column(x) for x in lst]
    def time_str_vals_int(self):
        self.cols[0].iter_str_vals()
    def time_str_vals_float(self):
        self.cols[1].iter_str_vals()
    def time_str_vals_str(self):
        self.cols[2].iter_str_vals()
