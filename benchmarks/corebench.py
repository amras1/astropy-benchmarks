from astropy.io.ascii import core

class CoreSuite:
    def setup(self):
        self.lines = []
        options = [['a b c d'], ['a b c \\', 'd'], ['a b \\', 'c \\', 'd'],
                   ['a b \\', 'c d'], ['a \\', 'b c \\', 'd']]
        for i in range(1000):
            self.lines.extend(options[i % 5])
        options = ['"a\tbc\t\td"', 'ab cd', '\tab\t\tc\td', 'a \tb \tcd']
        self.line = ''.join([options[i % 4] for i in range(1000)])
    def test_continuation_inputter(self):
        core.ContinuationLinesInputter().process_lines(self.lines)
    def test_whitespace_splitter(self):
        core.WhitespaceSplitter().process_line(self.line)
