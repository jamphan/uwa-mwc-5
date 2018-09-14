# uwaPySense
CITS4419 UWA

# Design documentation

See: [gh-pages](https://kjph.github.io/uwa-mwc-5/)

# Usage

Because this is a package, to run this locally, you will either need to install the pacakge through pip or run from the top-level directory (see [minimal python package structure](https://python-packaging.readthedocs.io/en/latest/minimal.html)).

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
  
  python -m pytest /tests/      # to run all unit tests with PyTest 
                                # Note, you may need to remove the db test or setup your own SQL server instance
  
  python -m tests.demonstration_bufferOverflow    # example run of a demonstration
```

## Installing with pip

Nb. **the package is still under construction. So there mabe issues**

``` bash

  cd /Path/to/repo/uwaPySense/
  
  python -m pip install -e .        # note the -e switch makes a symlink and not a proper install
                                    # this means when the package is updated, so too will the 'install'

```
