![memory map diagram](example_two_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(4, 39, 17)'>Blob4 (eMMC)</span>|0x100 (256)|0x30 (48)|0x85 (133)|||1:1|
|<span style='color:(48, 28, 3)'>Blob3 (DRAM)</span>|0x50 (80)|0x10 (16)|0x155 (341)|||1:1|
|<span style='color:(31, 34, 65)'>Blob5 (DRAM)</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|<span style='color:(8, 51, 21)'>Blob1 (eMMC)</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|<span style='color:(65, 17, 60)'>Blob2 (DRAM)</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|

---
#### eMMC:
- max address = 0x1B5 (437)
- Calculated from region data
#### DRAM:
- max address = 0x1B5 (437)
- Calculated from region data