# uwaPySense
CITS4419 UWA

# Usage

Because this is a package, to run this locally, you will either need to install the pacakge through pip or run from the top-level directory.

## Top-level directory

The top-level directory of the package (TLD) is where the `setup.py` file resides. 

``` bash
  cd /Path/to/repo/uwaPySense/
  ls
```

You should see the `setup.py` from the `ls` output in the TLD

From here you can run the package using the `-m` flag for the `python` interpreter

Examples:

``` bash

  python -m uwaPySense.main     # the main script for the server
  python -m pytests /tests/     # to run all unit tests with PyTest (you may need to remove the db test...)
  
  python -m tests.demonstration_bufferOverflow    # example run of a demonstration
```
