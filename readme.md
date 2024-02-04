[![Build](https://github.com/cracked-machine/mmdiagram/actions/workflows/python-app.yml/badge.svg)](https://github.com/cracked-machine/mmdiagram/actions/workflows/python-app.yml)
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

- Generate five regions called `kernel`, `rootfs`, `dtb`, `uboot` and `uboot-scr` where four of the five regions intersect/collide. The default report output path is used.

    ```
    python3 -m mmdiagram.generator kernel 0x10 0x50 rootfs 0x50 0x30 dtb 0x90 0x30 uboot 0xD0 0x50 uboot-scr 0x110 0x30
    ```

    ![](doc/example/report.png)

### Output

As well as the `png` format diagram image, a markdown report is also created:
- inline image of the diagram
- collision data table

An example can be found in [doc/example/report.md](doc/example/report.md)
