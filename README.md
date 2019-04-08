# dirimport: convenient library importer

## Install

- python -m venv your-dir
- cd your-dir
- ./bin/pip install dirimport

## Install (devel)

- git clone https://github.com/wtnb75/dirimport.git
- cd dirimport
- python -m venv .
- ./bin/pip install -r requirements.txt

## Use

- import dirimport
- mod = dirimport.importall("/path/to/dirname")

## import rules

- file.py -> `from .file import *`
- subpkg/ -> `from . import subpkg`
- do it recursively

then, all symbols will be accessible after import.

example:

- layout
  - symbol1 in dir/file1.py
  - symbol2 in dir/file2.py
  - symbol3 in dir/pkg/file1.py
- import
  - `import dir` with generated __init__.py
  - or `dir = dirimport.importall("dir")` without __init__.py
- result
  - symbol1 -> `dir.symbol1`
  - symbol2 -> `dir.symbol2`
  - symbol3 -> `dir.pkg.symbol2`

## CLI tools

```
# ./bin/dirimport-cli
Usage: dirimport-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  diff
  eval
  generate
```

- diff __init__.py
  - ./bin/dirimport-cli diff your-library-dir
- evaluate expression
  - ./bin/dirimport-cli eval your-library-dir 'expression'
- generate __init__.py
  - ./bin/dirimport-cli generate your-library-dir

## examples

- [ex1](examples/ex1.ipynb)
