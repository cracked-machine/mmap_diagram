![memory map diagram](A3_maxaddress_lower_than_memregions_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Flash|<span style='color:(41, 11, 41)'>Boot Image</span>|0xbb8 (3000)|0x7d0 (2000)|0x0 (0)||('Global System Address Map', 'OCM')|2:1|
|Global System Address Map|<span style='color:(64, 8, 65)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||1:1|
|Global System Address Map|<span style='color:(47, 24, 19)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|
