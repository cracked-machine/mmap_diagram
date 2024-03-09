![memory map diagram](example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(23, 8, 43)'>Blob4</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(67, 51, 47)'>Blob3</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(53, 40, 57)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(63, 35, 56)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(38, 26, 9)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
