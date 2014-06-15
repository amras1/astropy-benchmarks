Pandas
======

### Python ###

* `read_table` and `read_csv` come from `_make_parser_function()`, just with different default separation
* `_make_parser_function()` creates a function that calls `_read()`
* `_read()` calls `TextFileReader.read()`
* `TextFileReader` uses an engine for reading, which is `CParserWrapper` by default (`PythonParser` and `FixedWidthFieldParser` are others)
* `TextFileReader.read()` calls the `read()` function of its engine, instantiates a `DataFrame` with `col_dict`, `columns`, `index`
* `CParserWrapper.read()` calls `TextReader.read()` from `pandas.parser` (Cython/C)

### Cython ###
* `TextReader.__cinit__`:
```
self.parser = parser_new()
parser_init(self.parser)
```
* `TextReader.read`:
```
return self._read_rows(None, 1)
```
* `TextReader._read_rows`:
```
tokenize_all_rows(self.parser)
columns = self._convert_column_data()
if len(columns) > 0:
	rows_read = len(list(columns.values())[0])
	parser_consume_rows(self.parser, rows_read)
	parser_trim_buffers(self.parser)
	self.parser_start -= rows_read
return columns
```
* `TextReader._convert_column_data`:
```
num_cols = -1
for i in range(self.parser.lines):
	num_cols = max(num_cols, self.parsers.line_fields[i])
results = {}
for i in range(self.table_width):
	results[i] = self._convert_tokens(i)
```
* `TextReader._convert_tokens`:
```
col_res = None
for dt in ['<i8', '<f8', '|b1', '|08']:
	col_res = self._convert_with_dtype(dt, i)
	if col_res is not None:
		break
return col_res
```
* `TextReader._convert_with_dtype`:
```

```

### C ###
* `tokenize_all_rows`:
```
return _tokenize_helper(self, -1, 1);
```

* `_tokenize_helper`:
```
parser_op tokenize_bytes; // function of self, nrows
if (self->delim_whitespace)
	tokenize_bytes = tokenize_whitespace;
else if (self->lineterminator == '\0') // default
	tokenize_bytes = tokenize_delimited;
else
	tokenize_bytes = tokenize_delim_customterm;
while (1)
{
	if (self->datapos == self->datalen)
	{
		status = parser_buffer_bytes(self, self->chunksize); // input chunksize bytes at a time
		// puts the input bytes into self->data for handling, self->datalen has length
		if (status == REACHED_EOF)
		{
			parser_handle_eof(self);
			break;
		}
	}
	
	tokenize_bytes(self, nrows);
}
```

* `tokenize_delimited`:
```
for (/* all input bytes */)
{
	char c = /* next char */;
	switch (self->state)
	{
	// state machine handling here
	}
}
```

