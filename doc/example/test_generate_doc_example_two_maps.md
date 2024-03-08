![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(18, 16, 26)'>Blob4</span>|0x100 (256)|0x10 (16)|0x2d8 (728)|||1:1|
|DRAM|<span style='color:(37, 0, 2)'>Blob3</span>|0x50 (80)|0x10 (16)|0x388 (904)|||1:1|
|DRAM|<span style='color:(37, 12, 64)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(7, 51, 27)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(15, 21, 61)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
