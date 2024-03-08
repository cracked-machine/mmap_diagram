![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(64, 66, 9)'>Blob5</span>|0x78 (120)|0x20 (32)|0x350 (848)|||1:1|
|DRAM|<span style='color:(66, 47, 35)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(21, 7, 18)'>Blob7</span>|0x50 (80)|0x20 (32)|0x378 (888)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(59, 6, 60)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(61, 27, 57)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(36, 3, 32)'>Blob1</span>|0x0 (0)|0x20 (32)|0x3c8 (968)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(57, 56, 6)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
