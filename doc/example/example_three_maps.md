![memory map diagram](example_three_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(0, 25, 2)'>Blob5 (DRAM)</span>|0x78 (120)|0x20 (32)|0x0 (0)|||1:1|
|<span style='color:(26, 34, 14)'>Blob3 (DRAM)</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(40, 52, 64)'>Blob7 (flash)</span>|0x50 (80)|0x20 (32)|0x0 (0)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|<span style='color:(12, 46, 17)'>Blob4 (DRAM)</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|<span style='color:(57, 36, 39)'>Blob6 (flash)</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|<span style='color:(11, 4, 42)'>Blob1 (eMMC)</span>|0x0 (0)|0x20 (32)|0x0 (0)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|<span style='color:(8, 2, 67)'>Blob2 (DRAM)</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|

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