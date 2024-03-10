![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(13, 3, 17)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x2d2 (722)|||1:1|
|<span style='color:(41, 12, 64)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(13, 57, 49)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x2fa (762)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(51, 7, 5)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(51, 27, 57)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(39, 63, 1)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x34a (842)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(24, 31, 14)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

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