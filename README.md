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
  - symbol1 in dir1/file1.py
  - symbol2 in dir1/file2.py
  - symbol3 in dir1/pkg/file1.py
- import
  - `import dir1` with generated __init__.py
  - or `dir1 = dirimport.importall("dir1")` without __init__.py
- result
  - symbol1 -> `dir1.symbol1`
  - symbol2 -> `dir1.symbol2`
  - symbol3 -> `dir1.pkg.symbol2`

## CLI tools

```
# ./bin/dirimport
Usage: dirimport [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  diff
  eval
  generate
```

- diff `__init__.py`
  - ./bin/dirimport diff your-library-dir
- import and evaluate expression
  - ./bin/dirimport eval your-library-dir 'expression'
- generate `__init__.py`
  - ./bin/dirimport generate your-library-dir

## Use CLI command from docker

- docker run -v $PWD:/w -w /w ghcr.io/wtnb75/dirimport dirimport --help

## examples

- [ex1](examples/ex1.ipynb)

# Links

- [pypi](https://pypi.org/project/dirimport/)
- [coverage](https://wtnb75.github.io/dirimport/)
- [local pypi repo](https://wtnb75.github.io/dirimport/dist/)
