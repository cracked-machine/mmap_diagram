![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(67, 65, 6)'>Blob5</span>|0x78|0x20|0x350|||
|DRAM|<span style='color:(47, 14, 41)'>Blob3</span>|0x50|0x20|0x8|||
|flash|<span style='color:(54, 52, 49)'>Blob7</span>|0x50|0x20|0x378||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|
|DRAM|<span style='color:(54, 47, 22)'>Blob4</span>|0x28|0x20|0x8|||
|flash|<span style='color:(26, 11, 63)'>Blob6</span>|0xa|0x3c|0xa|||
|eMMC|<span style='color:(61, 8, 4)'>Blob1</span>|0x0|0x20|0x3c8||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|
|DRAM|<span style='color:(33, 26, 55)'>Blob2</span>|0x0|0x20|0x8|||
