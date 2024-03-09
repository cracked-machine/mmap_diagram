![memory map diagram](A3_region_exceeds_height-no_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(43, 62, 45)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||1:1|
|Global System Address Map|<span style='color:(24, 33, 21)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|
|Flash|<span style='color:(3, 61, 20)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||3382:1|
