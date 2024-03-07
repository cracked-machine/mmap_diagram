![memory map diagram](test_generate_doc_example_two_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|eMMC|<span style='color:(24, 7, 51)'>Blob4</span>|0x100|0x10|0x2d8|||
|DRAM|<span style='color:(60, 60, 59)'>Blob3</span>|0x50|0x10|0x388|||
|DRAM|<span style='color:(25, 24, 10)'>Blob5</span>|0x30|0x10|0x10|||
|eMMC|<span style='color:(35, 11, 59)'>Blob1</span>|0x10|0x10|0xe0||('DRAM', 'Blob2')<BR>('DRAM', 'Blob3')|
|DRAM|<span style='color:(58, 63, 7)'>Blob2</span>|0x10|0x10|0x10|||
