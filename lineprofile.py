from astropy.io import ascii
from cStringIO import StringIO

table = ascii.read('benchmarks/files/comparison/float.txt', format='basic')
s = StringIO()
ascii.write(table, s, Writer=ascii.Basic)
