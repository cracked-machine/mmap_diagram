![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(8, 53, 7)'>Blob5</span>|0x78 (120)|0x20 (32)|0x350 (848)|||1:1|
|DRAM|<span style='color:(1, 18, 57)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(11, 26, 64)'>Blob7</span>|0x50 (80)|0x20 (32)|0x378 (888)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(44, 2, 7)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(16, 54, 65)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(44, 28, 28)'>Blob1</span>|0x0 (0)|0x20 (32)|0x3c8 (968)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(17, 42, 66)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
