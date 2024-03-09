![memory map diagram](A6_region_exceeds_height-no_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(62, 11, 64)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||3:1|
|Global System Address Map|<span style='color:(15, 47, 14)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||3:1|
|Flash|<span style='color:(15, 24, 55)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||9598:1|
