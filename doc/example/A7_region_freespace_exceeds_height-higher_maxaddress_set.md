![memory map diagram](A7_region_freespace_exceeds_height-higher_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(50, 26, 64)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0xfffff04f (4294963279)|||4:1|
|<span style='color:(31, 56, 27)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|
|<span style='color:(23, 19, 27)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0xff000000 (4278190080)|||14176:1|

---
#### Global System Address Map:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input
#### Flash:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input