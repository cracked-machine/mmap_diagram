![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(55, 24, 54)'>Blob5</span>|0x78|0x20|0x350|||
|DRAM|<span style='color:(33, 38, 30)'>Blob3</span>|0x50|0x20|0x8|||
|flash|<span style='color:(43, 38, 7)'>Blob7</span>|0x50|0x20|0x378||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|
|DRAM|<span style='color:(5, 15, 17)'>Blob4</span>|0x28|0x20|0x8|||
|flash|<span style='color:(54, 44, 3)'>Blob6</span>|0xa|0x3c|0xa|||
|eMMC|<span style='color:(17, 53, 47)'>Blob1</span>|0x0|0x20|0x3c8||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|
|DRAM|<span style='color:(5, 35, 1)'>Blob2</span>|0x0|0x20|0x8|||
