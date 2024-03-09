![memory map diagram](example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(58, 23, 61)'>Blob5</span>|0x78 (120)|0x20 (32)|0x0 (0)|||1:1|
|DRAM|<span style='color:(37, 40, 52)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(22, 57, 33)'>Blob7</span>|0x50 (80)|0x20 (32)|0x0 (0)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(15, 10, 52)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(21, 24, 17)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(14, 25, 20)'>Blob1</span>|0x0 (0)|0x20 (32)|0x0 (0)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(43, 14, 52)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
