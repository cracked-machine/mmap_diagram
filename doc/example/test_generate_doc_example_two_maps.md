![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(54, 59, 6)'>Blob4</span>|0x100 (256)|0x10 (16)|0x2d8 (728)|||1:1|
|DRAM|<span style='color:(12, 41, 7)'>Blob3</span>|0x50 (80)|0x10 (16)|0x388 (904)|||1:1|
|DRAM|<span style='color:(64, 20, 3)'>Blob5</span>|0x30 (48)|0x10 (16)|0x10 (16)|||1:1|
|eMMC|<span style='color:(13, 53, 62)'>Blob1</span>|0x10 (16)|0x10 (16)|0xe0 (224)||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|1:1|
|DRAM|<span style='color:(41, 50, 42)'>Blob2</span>|0x10 (16)|0x10 (16)|0x10 (16)|||1:1|
