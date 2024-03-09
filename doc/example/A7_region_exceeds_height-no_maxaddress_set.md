![memory map diagram](A7_region_exceeds_height-no_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(68, 2, 35)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||4:1|
|Global System Address Map|<span style='color:(14, 7, 45)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|
|Flash|<span style='color:(12, 23, 51)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||13531:1|
