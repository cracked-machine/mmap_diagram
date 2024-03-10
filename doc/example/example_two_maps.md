![memory map diagram](example_two_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(35, 37, 34)'>Blob4 (eMMC)</span>|0x100 (256)|0x10 (16)|0x25a (602)|||1:1|
|<span style='color:(47, 45, 47)'>Blob3 (DRAM)</span>|0x50 (80)|0x10 (16)|0x30a (778)|||1:1|
|<span style='color:(53, 68, 4)'>Blob5 (DRAM)</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|<span style='color:(47, 6, 10)'>Blob1 (eMMC)</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|<span style='color:(32, 33, 9)'>Blob2 (DRAM)</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|

---
#### eMMC:
- max address = 0x36A (874)
- Calculated from region data
#### DRAM:
- max address = 0x36A (874)
- Calculated from region data