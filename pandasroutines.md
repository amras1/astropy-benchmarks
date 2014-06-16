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
	results[i] = self._convert_tokens(i, self.parser_start, self.parser.lines)
```
* `TextReader._convert_tokens`:
```
col_res = None
for dt in ['<i8', '<f8', '|b1', '|O8']:
	col_res = self._convert_with_dtype(dt, i, start, end)
	if col_res is not None:
		break
return col_res
```
* `TextReader._convert_with_dtype`:
```
if dtype[1] == 'i':
	return _try_int64(self.parser, i, start, end)
elif dtype[1] == 'f':
	return _try_double(self.parser, i, start, end)
elif dtype[1] == 'b':
	return _try_bool(self.parser, i, start, end)
elif dtype[1] == 'O':
	return self._string_convert(i, start, end)
```
* `_try_int64`, `_try_double`, `_try_bool`:
```
lines = line_end - line_start
result = np.empty(lines, dtype=np.int64) # np.float64, np.uint8
data = <int64_t *> result.data # <double *>, <uint8_t *>
cdef:
	coliter_t it
	char *word
	int error
coliter_setup(&it, parser, col, line_start)
for i in range(lines):
	word = COLITER_NEXT(it)
	data[i] = str_to_int64(word, INT64_MIN, INT64_MAX, &error)
	# or error = to_double(word, data, parser.sci, parser.decimal)
	# or error = to_boolean(word, data)
	# int:
	if error != 0:
		if error == ERROR_OVERFLOW:
			raise OverflowError(word)
		return None, None
	# double:
	if error != 1:
		if strcasecmp(word, cinf) == 0:
			data[0] = INF
		elif strcasecmp(word, cneginf) == 0:
			data[0] = NEGINF
		else:
			return None, None
		data += 1
	# bool:
	if error != 0:
		return None, None
	data += 1
return result # or result.view(np.bool_)
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

