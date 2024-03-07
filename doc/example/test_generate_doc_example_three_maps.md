![memory map diagram](test_generate_doc_example_three_maps_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|DRAM|<span style='color:(37, 56, 27)'>Blob5</span>|0x78|0x20|0x350|||
|DRAM|<span style='color:(53, 63, 0)'>Blob3</span>|0x50|0x20|0x8|||
|flash|<span style='color:(4, 25, 4)'>Blob7</span>|0x50|0x20|0x378||('DRAM', 'Blob3')<BR>('DRAM', 'Blob5')|
|DRAM|<span style='color:(39, 25, 20)'>Blob4</span>|0x28|0x20|0x8|||
|flash|<span style='color:(26, 34, 21)'>Blob6</span>|0xa|0x3c|0xa|||
|eMMC|<span style='color:(41, 35, 22)'>Blob1</span>|0x0|0x20|0x3c8||('DRAM', 'Blob2')<BR>('DRAM', 'Blob4')|
|DRAM|<span style='color:(6, 15, 35)'>Blob2</span>|0x0|0x20|0x8|||
