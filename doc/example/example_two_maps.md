![memory map diagram](example_two_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(24, 50, 5)'>Blob4 (eMMC)</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|<span style='color:(21, 31, 46)'>Blob3 (DRAM)</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|<span style='color:(46, 10, 55)'>Blob5 (DRAM)</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|<span style='color:(64, 7, 17)'>Blob1 (eMMC)</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|<span style='color:(11, 9, 52)'>Blob2 (DRAM)</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|

---
#### eMMC:
- max address = 0x110 (272)
- Calculated from region data
#### DRAM:
- max address = 0x60 (96)
- Calculated from region data