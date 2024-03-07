![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(65, 57, 17)'>Blob4</span>|0x100 (256)|0x10 (16)|0x2d8 (728)|||1:1|
|DRAM|<span style='color:(46, 20, 63)'>Blob3</span>|0x50 (80)|0x10 (16)|0x388 (904)|||1:1|
|DRAM|<span style='color:(53, 34, 63)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(41, 44, 26)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(27, 25, 5)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
