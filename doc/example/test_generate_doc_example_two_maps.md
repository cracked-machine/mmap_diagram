![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(68, 35, 61)'>Blob4</span>|0x100 (256)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(44, 24, 17)'>Blob3</span>|0x50 (80)|0x10 (16)|0x0 (0)|||1:1|
|DRAM|<span style='color:(51, 17, 61)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(51, 50, 34)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(29, 24, 65)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
