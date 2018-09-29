# uwaPySense
CITS4419 UWA

See: [gh-pages](https://kjph.github.io/uwa-mwc-5/)

## Contributing to docs

The documentation uses Sphinx (rsT). You will need to install 
the following packages

``` bash

$ python -m pip install sphinx
$ python -m pip install sphinx-rtd-theme

```

The source `.rst` files are found in `docs\source`. Edit these acoordingly.

The docs are then built using

``` bash
$ python -m sphinx source build -a
```

To publish the docs, you will need to move all items in `docs\build` to the `gh-pages` branch