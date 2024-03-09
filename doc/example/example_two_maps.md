![memory map diagram](example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(42, 46, 36)'>Blob4</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(3, 19, 15)'>Blob3</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(50, 31, 24)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(61, 21, 67)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(28, 63, 59)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
