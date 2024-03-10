![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(3, 22, 36)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x0 (0)|||1:1|
|<span style='color:(40, 26, 51)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(18, 8, 26)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x0 (0)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(32, 37, 39)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(5, 12, 65)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(29, 7, 32)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x0 (0)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(68, 46, 38)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

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