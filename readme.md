
### Setup

Run `sudo make init` to install python deps and linux packages.

### Usage:

Currently only CLI input data is supported. Data should be pairs of origin and size, one for each region to be plotted to the diagram.

```
python3 -m mmdiagram.generator 0x10 0x10 0x40 0xDD 0xCC 0xCC
```



### Output

As well as the `png` format diagram image, a markdown page is also created:
- inline image of the diagram
- table of the diagram data

An example can be found in [doc/example/report.md](doc/example/report.md)
