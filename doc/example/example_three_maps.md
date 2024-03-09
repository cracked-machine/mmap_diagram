![memory map diagram](example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(19, 68, 64)'>Blob5</span>|0x78 (120)|0x20 (32)|0x0 (0)|||1:1|
|DRAM|<span style='color:(17, 62, 42)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(19, 0, 27)'>Blob7</span>|0x50 (80)|0x20 (32)|0x0 (0)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(60, 16, 7)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(33, 64, 68)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(29, 24, 62)'>Blob1</span>|0x0 (0)|0x20 (32)|0x0 (0)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(32, 63, 18)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
