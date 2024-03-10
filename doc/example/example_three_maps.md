![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(59, 6, 20)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x2d2 (722)|||1:1|
|<span style='color:(44, 63, 38)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(28, 29, 41)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x2fa (762)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(34, 14, 27)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(40, 49, 48)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(68, 25, 24)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x34a (842)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(1, 1, 49)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

---
#### eMMC:
- max address = 0x36A (874)
- Calculated from region data
#### DRAM:
- max address = 0x36A (874)
- Calculated from region data
#### flash:
- max address = 0x36A (874)
- Calculated from region data