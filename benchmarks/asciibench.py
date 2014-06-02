from astropy.io import ascii

class ASCIISuite:
    def setup(self):
        self.tables = {}
        self.writers = {
            'csv': ascii.Csv,
            'rdb': ascii.Rdb,
            'fixed_width': ascii.FixedWidth,
            'fixed_width_no_header': ascii.FixedWidthNoHeader,
            'fixed_width_two_line': ascii.FixedWidthTwoLine,
            'tab': ascii.Tab,
            'no_header': ascii.NoHeader,
            'commented_header': ascii.CommentedHeader,
            'basic': ascii.Basic
            }
        for file_format in self.writers:
            for data_type in ('string', 'int', 'float'):
                self.tables[(file_format, data_type)] = self.read(
                    file_format, data_type)
                
    def read(self, file_format, data_type):
        return ascii.read('benchmarks/files/{}/{}.txt'.format(file_format,
                        data_type), format=file_format)

    def write(self, file_format, data_type):
        ascii.write(self.tables[(file_format, data_type)], 'output.txt',
                    Writer=self.writers[file_format])

    def time_csv_read_string(self):
        self.read('csv', 'string')

    def time_csv_read_int(self):
        self.read('csv', 'int')

    def time_csv_read_float(self):
        self.read('csv', 'float')

    def time_rdb_read_string(self):
        self.read('rdb', 'string')

    def time_rdb_read_int(self):
        self.read('rdb', 'int')

    def time_rdb_read_float(self):
        self.read('rdb', 'float')

    def time_fixedwidth_read_string(self):
        self.read('fixed_width', 'string')

    def time_fixedwidth_read_int(self):
        self.read('fixed_width', 'int')

    def time_fixedwidth_read_float(self):
        self.read('fixed_width', 'float')

    def time_fixedwidth_no_header_read_string(self):
        self.read('fixed_width_no_header', 'string')

    def time_fixedwidth_no_header_read_int(self):
        self.read('fixed_width_no_header', 'int')

    def time_fixedwidth_no_header_read_float(self):
        self.read('fixed_width_no_header', 'float')

    def time_fixedwidth_two_line_read_string(self):
        self.read('fixed_width_two_line', 'string')

    def time_fixedwidth_two_line_read_int(self):
        self.read('fixed_width_two_line', 'int')

    def time_fixedwidth_two_line_read_float(self):
        self.read('fixed_width_two_line', 'float')

    def time_tab_read_string(self):
        self.read('tab', 'string')

    def time_tab_read_int(self):
        self.read('tab', 'int')

    def time_tab_read_float(self):
        self.read('tab', 'float')

    def time_noheader_read_string(self):
        self.read('no_header', 'string')

    def time_noheader_read_int(self):
        self.read('no_header', 'int')

    def time_noheader_read_float(self):
        self.read('no_header', 'float')

    def time_commented_header_read_string(self):
        self.read('commented_header', 'string')

    def time_commented_header_read_int(self):
        self.read('commented_header', 'int')

    def time_commented_header_read_float(self):
        self.read('commented_header', 'float')

    def time_basic_read_string(self):
        self.read('basic', 'string')

    def time_basic_read_int(self):
        self.read('basic', 'int')

    def time_basic_read_float(self):
        self.read('basic', 'float')

    def time_sextractor_read_string(self):
        self.read('sextractor', 'string')

    def time_sextractor_read_int(self):
        self.read('sextractor', 'int')

    def time_sextractor_read_float(self):
        self.read('sextractor', 'float')

    def time_csv_write_string(self):
        self.write('csv', 'string')

    def time_csv_write_int(self):
        self.write('csv', 'int')

    def time_csv_write_float(self):
        self.write('csv', 'float')

    def time_rdb_write_string(self):
        self.write('rdb', 'string')

    def time_rdb_write_int(self):
        self.write('rdb', 'int')

    def time_rdb_write_float(self):
        self.write('rdb', 'float')

    def time_fixedwidth_write_string(self):
        self.write('fixed_width', 'string')

    def time_fixedwidth_write_int(self):
        self.write('fixed_width', 'int')

    def time_fixedwidth_write_float(self):
        self.write('fixed_width', 'float')

    def time_fixedwidth_no_header_write_string(self):
        self.write('fixed_width_no_header', 'string')

    def time_fixedwidth_no_header_write_int(self):
        self.write('fixed_width_no_header', 'int')

    def time_fixedwidth_no_header_write_float(self):
        self.write('fixed_width_no_header', 'float')

    def time_fixedwidth_two_line_write_string(self):
        self.write('fixed_width_no_header', 'string')

    def time_fixedwidth_two_line_write_int(self):
        self.write('fixed_width_no_header', 'int')

    def time_fixedwidth_two_line_write_float(self):
        self.write('fixed_width_no_header', 'float')

    def time_tab_write_string(self):
        self.write('tab', 'string')

    def time_tab_write_int(self):
        self.write('tab', 'int')

    def time_tab_write_float(self):
        self.write('tab', 'float')

    def time_noheader_write_string(self):
        self.write('no_header', 'string')

    def time_noheader_write_int(self):
        self.write('no_header', 'int')

    def time_noheader_write_float(self):
        self.write('no_header', 'float')

    def time_commented_header_write_string(self):
        self.write('commented_header', 'string')

    def time_commented_header_write_int(self):
        self.write('commented_header', 'int')

    def time_commented_header_write_float(self):
        self.write('commented_header', 'float')

    def time_basic_write_string(self):
        self.write('basic', 'string')

    def time_basic_write_int(self):
        self.write('basic', 'int')

    def time_basic_write_float(self):
        self.write('basic', 'float')
