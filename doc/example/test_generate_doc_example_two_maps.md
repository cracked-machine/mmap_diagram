![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(64, 68, 15)'>Blob4</span>|0x100|0x10|0x2d8|||
|DRAM|<span style='color:(34, 0, 19)'>Blob3</span>|0x50|0x10|0x388|||
|DRAM|<span style='color:(66, 43, 17)'>Blob5</span>|0x30|0x10|0x10|||
|eMMC|<span style='color:(24, 9, 38)'>Blob1</span>|0x10|0x10|0xe0||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|
|DRAM|<span style='color:(48, 11, 36)'>Blob2</span>|0x10|0x10|0x10|||
