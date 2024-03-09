![memory map diagram](A7_maxaddress_lower_than_memregions_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Flash|<span style='color:(23, 31, 4)'>Boot Image</span>|0xbb8 (3000)|0x7d0 (2000)|0x0 (0)||('Global System Address Map', 'OCM')|5:1|
|Global System Address Map|<span style='color:(4, 63, 32)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||4:1|
|Global System Address Map|<span style='color:(65, 23, 55)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|
