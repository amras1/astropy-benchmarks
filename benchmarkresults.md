Benchmarking
============
The asv benchmarks in astopy-benchmarks are separated into 3 types: comparison benchmarks, reading/writing benchmarks, and specific format benchmarks. They can be viewed in graph form [here](http://amras1.github.io/astropy-benchmarks/#).

Comparison benchmarks
---------------------

These benchmarks use 4 randomly generated text files to test reading and writing. One contains random integers from -500 to 500, one contains random floats from -500.0 to 500.0, one contains random 10-letter strings, and one contains a mixture of each type. All are 9 columns wide and 100,000 rows down. All times are in seconds.

#### Reading ####

Reader | float.txt | int.txt | string.txt | mixture.txt
--- | --- | --- | --- | ---
AstroPy | 0.670 | 0.710 | 0.678 | 0.653
numpy `genfromtxt()` | 0.550 | 0.621 | 0.403 | 0.881
numpy `loadtxt()` | 0.410 | 0.543 | 0.369 | 0.618
pandas `read_csv()` | 0.112 | 0.056 | 0.257 | 0.154
pandas `read_table()` | 0.114 | 0.055 | 0.254 | 0.149

#### Writing ####

Writer | float.txt | int.txt | string.txt | mixture.txt
--- | --- | --- | --- | ---
AstroPy | 1.779 | 2.350 | 0.939 | 1.684
numpy | 0.900 | 0.629 | 0.429 | 0.568
pandas | 0.643 | 0.137 | 0.164 | 0.327

As expected, AstroPy is currently slower than both numpy and pandas for both reading and writing text-based data. However, numpy's ``genfromtxt()`` is slower than ``ascii.read()`` when ``dtype=None`` (which forces numpy to infer the data types of columns), as shown by the 0.881 seconds it takes ``genfromtxt()`` to read the mixed file rather than 0.653 seconds for AstroPy. Aside from this, the hierarchy of speed appears to be ``read_csv()`` > ``read_table()`` >> ``loadtxt()`` > ``genfromtxt()`` > ``ascii.read()``. The pandas routines are nearly identical in terms of speed, which I assume is because they share the same underlying implementation.

It's also interesting to note the differences between data types. AstroPy reads each type in approximately the same amount of time, but it writes strings more quickly and integers more slowly. numpy's order of speed is string > float > int for reading and string > int > float for writing, while pandas' order of speed is int > float > string for reading and int > string > float for writing. The fact that each library is different suggests that they have different approaches to recognizing data types and performing conversions, which I'll be exploring next week with pandas. Incidentally, the pandas routines use ``DataFrame`` instead of ``Table`` (which both AstroPy and numpy use), so some of the inefficiency of AstroPy's and numpy's function calls could have to do with the inefficiency of data storage in ``Table``.

Reading/writing benchmarks
--------------------------

#### Reading ####

Format | float.txt | int.txt | string.txt
--- | --- | --- | ---
CSV | 0.12 | 0.125 | 0.115
RDB |0.095 | 0.100 | 0.069
Fixed width | 0.145 | 0.145 | 0.134
Fixed width, no header | 0.136 | 0.148 | 0.129
Fixed width, two line header | 0.136 | 0.149 | 0.130
Tab-separated | 0.091 | 0.101 | 0.081
No header | 0.125 | 0.130 | 0.125
Commented header | 0.121 | 0.131 | 0.116
Basic | 0.127 | 0.134 | 0.113
IPAC | 0.130 | 0.157 | 0.118
SExtractor | 0.127 | 0.134 | 0.117
LaTeX | 0.139 | 0.152 | 0.133
AASTex | 0.139 | 0.152 | 0.131

#### Writing ####

Format | float.txt | int.txt | string.txt
--- | --- | --- | ---
CSV | 0.372 | 0.507 | 0.208
RDB | 0.373 | 0.504 | 0.197
Fixed width | 0.396 | 0.547 | 0.217
Fixed width, no header | 0.412 | 0.535 | 0.215
Fixed width, two line header | 0.399 | 0.526 | 0.223
Tab-separated | 0.387 | 0.515 | 0.202
No header | 0.371 | 0.519 | 0.194
Commented header | 0.372 | 0.548 | 0.192
Basic | 0.383 | 0.504 | 0.196
IPAC | 0.371 | 0.514 | 0.195
LaTeX | 0.336 | 0.502 | 0.173
AASTex | 0.332 | 0.489 | 0.172

As with the comparison benchmarks, the hierarchy of speed seemed to be string > float > int for writing. Reading times didn't vary considerably, but strings tended to be a little faster than floats or ints. Variations across different formats were actually less than I had expected (although RDB and tab-separated were faster for reading and LaTeX/AASTex were faster for writing), which suggests that the readers and writers share performance bottlenecks. Improving the efficiency of the main algorithm, currently in ``core.py`` and ``ui.py``, should speed up reading and writing across the board.

Specific benchmarks
-------------------
####``CoreSuite``####
* `time_continuation_inputter`: 629 μs
* `time_whitespace_splitter`: 834 μs
* `time_default_splitter_call`: 648 ns
* `time_base_splitter`: 260 ns
* `time_convert_vals`: 3.85 μs

####``FixedWidthSuite``####
* `time_splitter`: 62.8 μs
* `time_header`: 47.8 μs

####``IPACSuite``####
* `time_splitter`: 248 μs
* `time_get_cols`: 977 μs
* `time_header_str_vals`: 110 μs
* `time_data_str_vals`: 118 ms

####``RDBSuite``####
* `time_get_cols`: 2.19 ms

####``SExtractorSuite``####
* `time_header`: 2.19 ms

####``TableSuite``####
* `time_str_vals_float`: 335 ns
* `time_str_vals_int`: 342 ns
* `time_str_vals_str`: 342 ns
* `time_table_init_from_list`: 592 μs
* `time_table_outputter`: 720 μs
* `mem_table_init`: 6440 bytes
* `mem_table_outputter`: 6440 bytes

These turned out to be fairly negligible in terms of time, with the exception of `time_data_str_vals` -- perhaps that can be rewritten more efficiently.

Profiling
=========

I ran cProfile for a quick high-level overview with the following code:
```
import cProfile
from astropy.io import ascii
cProfile.run('t = ascii.read("benchmarks/files/comparison/float.txt", format="basic")',
             'readstats')
cProfile.run('ascii.write(t, "out.txt", Writer=ascii.Basic)', 'writestats')
```

I then used [SnakeViz](http://jiffyclub.github.io/snakeviz/), a profiling visualization tool, to interpret the results and get a sense for which routines are performance benchmarks.

Reading
-------
[Here](http://i.imgur.com/DRuB3SR.png) is a screenshot of SnakeViz's output using the results of profiling `ascii.read()` with cProfile. The inner tan-colored ring is the method `read()` in `BaseReader()`, which takes up virtually of the time discounting the negligible overhead of higher-level functions `ascii.read()` and `_guess()`. `read()` calls a number of functions, but the most significant in terms of time are `DefaultSplitter.__call__()` (dark blue, taking up a cumulative 40% of the total time), `TableOutputter.__call__()` (light blue, taking up a cumulative 20% of the total time), and `read()` itself (taking up 19% of the total time). Futhermore, `DefaultSplitter.__call__()` is broken up into `BaseSplitter.process_val()` (39%), internal processing (56%), and the fairly negligible `DefaultSplitter.process_line()`. `BaseData.masks()` and `BaseData.get_data_lines()` are next in terms of time consumption, although they both take up less than 8% of the total time in `read()`.

Writing
-------
[Here](http://i.imgur.com/HCfw5lJ.png) is a similar screenshot of SnakeViz's output for `ascii.write()`. The innermost circle is `BaseReader.write()` and the enclosing ring is `BaseData.write()`, which takes up virtually all of the writing time. This is split into `BaseColumn.iter_str_vals()` (light blue on the right, taking up 62%) and `DefaultSplitter.join()` (blue-green on the left, taking up 28%), followed by `BaseData._replace_vals()` and `BaseData.write()` itself. `BaseColumn.iter_str_vals()` ultimately boils down to a lambda function repeatedly called in `_pformat_col_iter()` as well as some time spent in `_pformat_col_iter()` itself, while `DefaultSplitter.join()` is split into `BaseSplitter.process_val()`, the `writerow()` method in `csv.writer`, and its own processing.
