![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(22, 37, 62)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x0 (0)|||1:1|
|<span style='color:(67, 30, 51)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(6, 19, 41)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x0 (0)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(27, 26, 56)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(23, 57, 7)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(59, 12, 37)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x0 (0)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(54, 39, 9)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

---
#### eMMC:
- max address = 0x20 (32)
- Calculated from region data
#### DRAM:
- max address = 0x98 (152)
- Calculated from region data
#### flash:
- max address = 0x70 (112)
- Calculated from region data