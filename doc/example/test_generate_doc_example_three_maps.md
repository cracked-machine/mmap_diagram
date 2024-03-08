![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(19, 58, 62)'>Blob5</span>|0x78 (120)|0x20 (32)|0x350 (848)|||1:1|
|DRAM|<span style='color:(61, 54, 56)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(56, 54, 23)'>Blob7</span>|0x50 (80)|0x20 (32)|0x378 (888)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(66, 20, 16)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(46, 13, 38)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(6, 46, 8)'>Blob1</span>|0x0 (0)|0x20 (32)|0x3c8 (968)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(19, 40, 3)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
