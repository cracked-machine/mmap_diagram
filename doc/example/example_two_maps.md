![memory map diagram](example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(19, 68, 42)'>Blob4</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(29, 68, 60)'>Blob3</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(5, 44, 42)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(13, 18, 44)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(5, 25, 64)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
