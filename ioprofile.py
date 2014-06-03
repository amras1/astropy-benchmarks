from astropy.io import ascii

table = ascii.read('benchmarks/files/csv/string.txt', format='csv')
ascii.write(table, 'output.txt', Writer=ascii.Csv)
