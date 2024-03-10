![memory map diagram](A6_region_freespace_exceeds_height-higher_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(53, 6, 5)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0xfffff04f (4294963279)|||3:1|
|<span style='color:(41, 28, 57)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||3:1|
|<span style='color:(15, 18, 61)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0xff000000 (4278190080)|||10056:1|

---
#### Global System Address Map:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input
#### Flash:
- max address = 0xFFFFFFFF (4,294,967,295)
- User-defined input