import cProfile
from astropy.io import ascii
cProfile.run('t=ascii.read("benchmarks/files/comparison/float.txt", ' \
             'format="basic")', 'readstats')
cProfile.run('ascii.write(t, "out.txt", Writer=ascii.Basic)', 'writestats')
