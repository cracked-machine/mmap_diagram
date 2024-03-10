![memory map diagram](example_two_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(51, 27, 48)'>Blob4 (eMMC)</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|<span style='color:(4, 66, 2)'>Blob3 (DRAM)</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|<span style='color:(21, 30, 12)'>Blob5 (DRAM)</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|<span style='color:(26, 18, 14)'>Blob1 (eMMC)</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|<span style='color:(45, 44, 42)'>Blob2 (DRAM)</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|

---
#### eMMC:
- max address = 0x110 (272)
- Calculated from region data
#### DRAM:
- max address = 0x60 (96)
- Calculated from region data