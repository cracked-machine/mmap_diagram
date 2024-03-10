![memory map diagram](example_two_maps_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(47, 52, 1)'>Blob4 (eMMC)</span>|0x100 (256)|0x10 (16)|0x25a (602)|||1:1|
|<span style='color:(60, 65, 29)'>Blob3 (DRAM)</span>|0x50 (80)|0x10 (16)|0x30a (778)|||1:1|
|<span style='color:(29, 24, 56)'>Blob5 (DRAM)</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|<span style='color:(25, 51, 59)'>Blob1 (eMMC)</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|<span style='color:(50, 60, 24)'>Blob2 (DRAM)</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|

---
#### eMMC:
- max address = 0x36A (874)
- Calculated from region data
#### DRAM:
- max address = 0x36A (874)
- Calculated from region data