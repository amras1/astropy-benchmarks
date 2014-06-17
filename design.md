Parsing Overview
================


##Cython##

* `__cinit__()` initializes `CParser` based on supplied parameters as well as the tokenizer.
* `setup_tokenizer()` passes a supplied source object (filename, file-like object, single string, or list of strings) to the tokenizer for future processing.
* `read_header()` uses the tokenizer to get column names, which it stores in `self.names`. If `header=None`, it tries to detect the number of columns from the first line of data and autogenerates the column names. `self.names` is then adjusted based on `include_names` and `exclude_names`, as unwanted columns are thrown out.
* `read()` invokes the tokenizer, then calls `_convert_data()` and returns the result.
* `_convert_data()` tries calling `convert_int()`, `convert_float()`, and `convert_str()` on each column in that order, returning the first one which works correctly.
* `convert_int()` puts column data in an `ndarray` with `dtype=np.int_` and operates on an `int *` pointer to its `data` attribute. It loops through each field in the column (by calling C functions) and replaces values if necessary as determined by `fill_values`, `fill_include_names`, and `fill_exclude_names`; in this case, it also marks the column as masked. It then calls `str_to_long()`, a C function, to try to perform conversion. If this fails, `convert_int` raises a `ValueError`. If it successfully converts all of the data, `convert_int()` returns either an `ndarray` or a `masked_array`, depending on whether any values are masked.
* `convert_float()` and `convert_str()` work similarly, except `convert_str()` performs no conversion and simply creates an `ndarray` with `dtype='|S{0}'.format(n)` where `n` is the length of the longest field value.


##C##
A struct called `tokenizer_t` contains tokenizing information and is a parameter in all tokenizing functions. More importantly, `tokenizer_t` encapsulates the actual data created during the tokenization algorithm in an array of strings: `char **output_cols`. Each string in the array represents a table column, with field values separated by `'\x00'` delimiters, and the struct contains information about the number of columns as well as both the logical and actual size of each column string (the actual size doubles when necessary using `realloc()`). The struct also contains `tokenizer_state state`, an enum which contains the current state of the tokenizer and is important for state-machine handling, as well as relevant tokenizing parameters like `quotechar` and `delimiter`. Similar attributes exist specific to header parsing.

###General tokenizing strategy###
The main loop in `tokenize()` repeatedly gets the next `char` available for input and processes it with state-machine logic using a `switch` statement. Here is a basic pseudocode version of the loop:
```
while not done with parsing:
    c = next char to be processed
    repeat = True
    while repeat and not done: // Potentially repeat parsing in a different tokenizing state
        repeat = 0
        switch (state):
        START_LINE:
            if c is whitespace:
                do nothing
            else if c == comment:
                state = COMMENT
            initialize row information
            state = START_FIELD
            repeat = True
        START_FIELD:
            if c is whitespace:
                do nothing
            else if c == delimiter:
                end field
            else if c == quotechar:
                state = START_QUOTED_FIELD
            else:
                state = FIELD
                repeat = True
        case START_QUOTED_FIELD:
            if c is whitespace:
                do nothing
            else if c == quotechar:
                end field
            slse:
                state = QUOTED_FIELD
                repeat = True
        case FIELD:
            if c == delimiter:
                end field
                state = START_FIELD
            else if c == '\n':
                end field and line
                state = START_LINE
            else:
                add c to the current column string
        case QUOTED_FIELD:
            if c == quotechar:
                state = FIELD
            else if c == '\n':
                state = QUOTED_FIELD_NEWLINE
            else:
                add c to the current column string
        case QUOTED_FIELD_NEWLINE:
            if c is whitespace or '\n':
                do nothing
            else if c == quotechar:
                state = FIELD
            else:
                repeat = 1
                state = QUOTED_FIELD
        case COMMENT:
            if c == '\n':
                state = START_LINE
                

```
