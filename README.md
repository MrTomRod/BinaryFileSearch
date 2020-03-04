# BinaryFileSearch - Query sorted files in a RAM-efficient way!

Binary search algorithm for big sorted files that cannot be read into RAM.

## Requirements:

* file must be **sorted by the first column**. (in bash: `sort --key=1 --field-separator=\t --output=file.txt.sorted file.txt`)
* every line must begin with the sorted string/integer, followed by a separator.
* there may be multiple lines beginning with the same string/integer. (the script will return a list of lines that start with the same string/integer)

## Installation:

```bash
pip install binary_file_search
```

## Usage:

```Python
from binary_file_search.BinaryFileSearch import BinaryFileSearch
bfs = BinaryFileSearch('/path/to/file', sep="\t")
lines = bfs.extract_lines_beginning_with('query')  # get lines that begin with 'query':
```

Tip: `run bfs.close_file()` after usage.

### Parameters

| Parameter      | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `file`         | path to the sorted file to be searched                              |
| `sep`          | separator (default: `"\t"`)                                         |
| `string_mode`  | `True` if the sorted column consists of strings, `False` if integers|
| `query`        | string/integer to search                                            |

### Results

The function returns a of lines, the lines being separated by paramter `sep`, for example:
```Python
[
    ['query', 'l1_col2', 'l1_col3', ...],  # first line that starts with 'query'
    ['query', 'l2_col2', 'l2_col3', ...],  # second line that starts with 'query'
    ...
]
```

If the query cannot be found, a `KeyError` is raised.

## Credit:
Inspired by https://www.geeksforgeeks.org/python-program-for-binary-search/

## Licence:

MIT License

Copyright (c) 2020 Thomas Roder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.