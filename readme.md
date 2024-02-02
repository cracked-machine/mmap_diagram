
### Setup

Run `sudo make init` to install python deps and linux packages.

### Usage:

```
python3 -m mmdiagram.generator 0x10 0x10 0x40 0xDD 0xCC 0xCC
```
### Output

```
Origin:16,Size:16 - palegoldenrod
Origin:64,Size:221 - olivedrab
Origin:204,Size:204 - darkslategray
```

### Generated Diagram

![](out.png)

### Tests

Run `make tests`