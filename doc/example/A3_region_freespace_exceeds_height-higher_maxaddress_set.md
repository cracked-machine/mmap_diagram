![memory map diagram](A3_region_freespace_exceeds_height-higher_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(26, 41, 37)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0xfffff04f (4294963279)|||1:1|
|<span style='color:(22, 33, 0)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|
|<span style='color:(31, 13, 28)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0xff000000 (4278190080)|||3544:1|

---
#### Global System Address Map:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input
#### Flash:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input