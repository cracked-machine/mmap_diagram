![memory map diagram](A4_region_freespace_exceeds_height-higher_maxaddress_set_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(22, 54, 64)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0xfffff04f (4294963279)|||2:1|
|Global System Address Map|<span style='color:(0, 14, 54)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||2:1|
|Flash|<span style='color:(32, 48, 17)'>Boot Image</span>|0x0 (0)|0xffffff (16777215)|0xff000000 (4278190080)|||5011:1|
