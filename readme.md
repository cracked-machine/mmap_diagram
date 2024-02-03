[![Codecov](https://img.shields.io/codecov/c/github/cracked-machine/mmdiagram)](https://app.codecov.io/gh/cracked-machine/mmdiagram)

### Setup

Run `sudo make init` to install python deps and linux packages.

### Usage:

```
usage: generator.py [-h] [-o OUT] [regions ...]

positional arguments:
regions            command line input for regions should be tuples of name, origin and size.

options:
-h, --help         show this help message and exit
-o OUT, --out OUT  path to the markdown output report file. Defaults to "out/report.md"
```

- Generate three regions called `kernel`, `rootfs` and `dtb` to default report output path.

    ```
    python3 -m mmdiagram.generator kernel 0x10 0x10 rootfs 0x40 0xDD dtb 0xCC 0xCC
    ```



### Output

As well as the `png` format diagram image, a markdown page is also created:
- inline image of the diagram
- table of the diagram data

An example can be found in [doc/example/report.md](doc/example/report.md)
