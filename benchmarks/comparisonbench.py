from astropy.io import ascii
from cStringIO import StringIO
import numpy as np
import pandas

class ComparisonSuite:
    def setup(self):
        self.mix_dtype = np.dtype({'names': '123456789', 'formats':
                ('i4', 'f4', 'S10', 'i4', 'f4', 'S10', 'i4', 'f4', 'S10')})
        self.data = {}
        for datatype in ('float', 'int', 'string', 'mixture'):
            f = open('benchmarks/files/comparison/{}.txt'.format(datatype))
            self.data[datatype] = f.read()
            f.close()
                                  
    def time_astropy_float(self):
        ascii.read(StringIO(self.data['float']), format='basic')
                                  
    def time_astropy_int(self):
        ascii.read(StringIO(self.data['int']), format='basic')
                                  
    def time_astropy_string(self):
        ascii.read(StringIO(self.data['string']), format='basic')

    def time_astropy_mixture(self):
        ascii.read(StringIO(self.data['mixture']), format='basic')

    def time_numpy_loadtxt_float(self):
        np.loadtxt(StringIO(self.data['float']), delimiter=' ')

    def time_numpy_loadtxt_int(self):
        np.loadtxt(StringIO(self.data['int']), delimiter=' ',
                   dtype='i4')

    def time_numpy_loadtxt_string(self):
        np.loadtxt(StringIO(self.data['string']), delimiter=' ',
                   dtype='S10')

    def time_numpy_loadtxt_mixture(self):
        np.loadtxt(StringIO(self.data['mixture']), delimiter=' ',
                   dtype=self.mix_dtype)

    def time_numpy_genfromtxt_float(self):
        np.genfromtxt(StringIO(self.data['float']), delimiter=' ')

    def time_numpy_genfromtxt_int(self):
        np.genfromtxt(StringIO(self.data['int']), delimiter=' ',
                      dtype='i4')

    def time_numpy_genfromtxt_string(self):
        np.genfromtxt(StringIO(self.data['string']), delimiter=' ',
                      dtype='S10')

    def time_numpy_genfromtxt_mixture(self):
        # Test out genfromtxt's autoconversion
        np.genfromtxt(StringIO(self.data['mixture']), delimiter=' ',
                      dtype=None)

    def time_pandas_read_table_float(self):
        pandas.read_table(StringIO(self.data['float']), sep=' ')

    def time_pandas_read_table_int(self):
        pandas.read_table(StringIO(self.data['int']), sep=' ')

    def time_pandas_read_table_string(self):
        pandas.read_table(StringIO(self.data['string']), sep=' ')

    def time_pandas_read_table_mixture(self):
        pandas.read_table(StringIO(self.data['mixture']), sep=' ')

    def time_pandas_read_csv_float(self):
        pandas.read_csv(StringIO(self.data['float']), sep=' ')

    def time_pandas_read_csv_int(self):
        pandas.read_csv(StringIO(self.data['int']), sep=' ')

    def time_pandas_read_csv_string(self):
        pandas.read_csv(StringIO(self.data['string']), sep=' ')

    def time_pandas_read_csv_mixture(self):
        pandas.read_csv(StringIO(self.data['mixture']), sep=' ')
