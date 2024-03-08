![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(31, 11, 20)'>Blob4</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(47, 4, 62)'>Blob3</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(36, 35, 30)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(10, 53, 34)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(33, 5, 35)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
