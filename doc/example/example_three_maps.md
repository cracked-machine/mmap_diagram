![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(29, 64, 50)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x11d (285)|||1:1|
|<span style='color:(42, 53, 48)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(48, 39, 61)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x145 (325)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(49, 34, 66)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(8, 46, 30)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(1, 23, 18)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x195 (405)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(38, 47, 0)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

---
#### eMMC:
- max address = 0x1B5 (437)
- Calculated from region data
#### DRAM:
- max address = 0x1B5 (437)
- Calculated from region data
#### flash:
- max address = 0x1B5 (437)
- Calculated from region data