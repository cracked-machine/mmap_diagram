![memory map diagram](A8_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(28, 45, 55)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||5:1|
|<span style='color:(45, 23, 56)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||5:1|
|<span style='color:(53, 41, 59)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||19196:1|

---
#### Global System Address Map:
- max address = 0xFB0 (4,016)
- Calculated from region data
#### Flash:
- max address = 0xFFFFFF (16,777,215)
- Calculated from region data