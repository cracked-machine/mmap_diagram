![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(58, 43, 33)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x2d2 (722)|||1:1|
|<span style='color:(61, 9, 16)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(44, 37, 31)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x2fa (762)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(14, 63, 32)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(53, 42, 24)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(28, 36, 31)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x34a (842)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(63, 47, 43)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

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