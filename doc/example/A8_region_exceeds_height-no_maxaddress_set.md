![memory map diagram](A8_region_exceeds_height-no_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(45, 59, 33)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||5:1|
|Global System Address Map|<span style='color:(11, 23, 28)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||5:1|
|Flash|<span style='color:(34, 26, 4)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||19196:1|
