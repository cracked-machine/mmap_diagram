![memory map diagram](A7_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(0, 36, 50)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||4:1|
|<span style='color:(61, 67, 19)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|
|<span style='color:(49, 0, 66)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|0x0 (0)|||13531:1|

---
#### Global System Address Map:
- max address = 0xFB0 (4,016)
- Calculated from region data
#### Flash:
- max address = 0xFFFFFF (16,777,215)
- Calculated from region data