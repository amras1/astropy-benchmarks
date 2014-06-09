import os.path
from astropy.io import ascii

writer_dict = {
    'commented_header': ascii.CommentedHeader,
    'fixed_width': ascii.FixedWidth,
    'fixed_width_no_header': ascii.FixedWidthNoHeader,
    'fixed_width_two_line': ascii.FixedWidthTwoLine,
    'no_header': ascii.NoHeader,
    'rdb': ascii.Rdb,
    'tab': ascii.Tab,
    'basic': ascii.Basic,
    'ipac': ascii.Ipac,
    'latex': ascii.Latex,
    'aastex': ascii.AASTex
}

for ftype in writer_dict:
    for name in ('string', 'int', 'float'):
        if not os.path.isfile('benchmarks/files/{}/{}.txt'.format(ftype, name)):
            print 'Converting csv/{}.txt to {} format'.format(name, ftype)
            t = ascii.read('benchmarks/files/csv/{}.txt'.format(name), format='csv')
            ascii.write(t, 'benchmarks/files/{}/{}.txt'.format(ftype, name),
                        Writer=writer_dict[ftype])
