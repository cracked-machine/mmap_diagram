![memory map diagram](A3_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(56, 5, 56)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||1:1|
|<span style='color:(50, 11, 45)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|
|<span style='color:(34, 28, 47)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||3382:1|

---
#### Global System Address Map:
- max address = 0xFB0 (4,016)
- Calculated from region data
#### Flash:
- max address = 0xFFFFFF (16,777,215)
- Calculated from region data