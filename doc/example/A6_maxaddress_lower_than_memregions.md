![memory map diagram](A6_maxaddress_lower_than_memregions_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Flash|<span style='color:(10, 67, 41)'>Boot Image</span>|0xbb8 (3000)|0x7d0 (2000)|0x0 (0)||('Global System Address Map', 'OCM')|3:1|
|Global System Address Map|<span style='color:(26, 37, 22)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||3:1|
|Global System Address Map|<span style='color:(25, 21, 10)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||3:1|
