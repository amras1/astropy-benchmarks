from astropy.io import ascii
import numpy as np
import pandas

class ComparisonSuite:
    def setup(self):
        self.mix_dtype = np.dtype({'names': '123456789', 'formats':
                ('i4', 'f4', 'S10', 'i4', 'f4', 'S10', 'i4', 'f4', 'S10')})
                                  
    def time_astropy_float(self):
        ascii.read('benchmarks/files/comparison/float.txt', format='basic')
                                  
    def time_astropy_int(self):
        ascii.read('benchmarks/files/comparison/int.txt', format='basic')
                                  
    def time_astropy_string(self):
        ascii.read('benchmarks/files/comparison/string.txt', format='basic')

    def time_astropy_mixture(self):
        ascii.read('benchmarks/files/comparison/mixture.txt', format='basic')

    def time_numpy_loadtxt_float(self):
        np.loadtxt('benchmarks/files/comparison/float.txt', delimiter=' ')

    def time_numpy_loadtxt_int(self):
        np.loadtxt('benchmarks/files/comparison/int.txt', delimiter=' ',
                   dtype='i4')

    def time_numpy_loadtxt_string(self):
        np.loadtxt('benchmarks/files/comparison/string.txt', delimiter=' ',
                   dtype='S10')

    def time_numpy_loadtxt_mixture(self):
        np.loadtxt('benchmarks/files/comparison/mixture.txt', delimiter=' ',
                   dtype=self.mix_dtype)

    def time_numpy_genfromtxt_float(self):
        np.genfromtxt('benchmarks/files/comparison/float.txt', delimiter=' ')

    def time_numpy_genfromtxt_int(self):
        np.genfromtxt('benchmarks/files/comparison/int.txt', delimiter=' ',
                      dtype='i4')

    def time_numpy_genfromtxt_string(self):
        np.genfromtxt('benchmarks/files/comparison/string.txt', delimiter=' ',
                      dtype='S10')

    def time_numpy_genfromtxt_mixture(self):
        np.genfromtxt('benchmarks/files/comparison/mixture.txt', delimiter=' ',
                      dtype=None) # Test out genfromtxt's autoconversion

    def time_pandas_read_table_float(self):
        pandas.read_table('benchmarks/files/comparison/float.txt', sep=' ')

    def time_pandas_read_table_int(self):
        pandas.read_table('benchmarks/files/comparison/int.txt', sep=' ')

    def time_pandas_read_table_string(self):
        pandas.read_table('benchmarks/files/comparison/string.txt', sep=' ')

    def time_pandas_read_table_mixture(self):
        pandas.read_table('benchmarks/files/comparison/mixture.txt', sep=' ')

    def time_pandas_read_csv_float(self):
        pandas.read_csv('benchmarks/files/comparison/float.txt', sep=' ')

    def time_pandas_read_csv_int(self):
        pandas.read_csv('benchmarks/files/comparison/int.txt', sep=' ')

    def time_pandas_read_csv_string(self):
        pandas.read_csv('benchmarks/files/comparison/string.txt', sep=' ')

    def time_pandas_read_csv_mixture(self):
        pandas.read_csv('benchmarks/files/comparison/mixture.txt', sep=' ')
