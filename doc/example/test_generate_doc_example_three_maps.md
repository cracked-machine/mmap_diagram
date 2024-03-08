![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(52, 54, 54)'>Blob5</span>|0x78 (120)|0x20 (32)|0x350 (848)|||1:1|
|DRAM|<span style='color:(4, 45, 43)'>Blob3</span>|0x50 (80)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(41, 54, 7)'>Blob7</span>|0x50 (80)|0x20 (32)|0x378 (888)||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|1:1|
|DRAM|<span style='color:(30, 25, 31)'>Blob4</span>|0x28 (40)|0x20 (32)|0x8 (8)|||1:1|
|flash|<span style='color:(25, 3, 53)'>Blob6</span>|0xa (10)|0x3c (60)|0xa (10)|||1:1|
|eMMC|<span style='color:(28, 66, 39)'>Blob1</span>|0x0 (0)|0x20 (32)|0x3c8 (968)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|1:1|
|DRAM|<span style='color:(15, 1, 51)'>Blob2</span>|0x0 (0)|0x20 (32)|0x8 (8)|||1:1|
