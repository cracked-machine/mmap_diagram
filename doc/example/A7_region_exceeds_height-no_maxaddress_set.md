![memory map diagram](A7_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(14, 29, 32)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0xad8 (-2776)| end @ 0x4d8 ||4:1|
|<span style='color:(20, 23, 24)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|
|<span style='color:(60, 32, 38)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xfffb27 (-16775975)| end @ 0x4d8 ||13531:1|

---
#### Global System Address Map:
- max address = 0x4D8 (1,240)
- Calculated from region data
#### Flash:
- max address = 0x4D8 (1,240)
- Calculated from region data