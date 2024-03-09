![memory map diagram](A8_region_freespace_exceeds_height-higher_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(18, 68, 7)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0xfffff04f (4294963279)|||5:1|
|Global System Address Map|<span style='color:(27, 51, 25)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||5:1|
|Flash|<span style='color:(3, 5, 18)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0xff000000 (4278190080)|||20112:1|
