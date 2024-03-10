![memory map diagram](A8_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(59, 63, 8)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0xc46 (-3142)| end @ 0x36a ||5:1|
|<span style='color:(4, 59, 0)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|-0x8e (-142)| end @ 0x36a ||5:1|
|<span style='color:(36, 50, 57)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xfffc95 (-16776341)| end @ 0x36a ||19196:1|

---
#### Global System Address Map:
- max address = 0x36A (874)
- Calculated from region data
#### Flash:
- max address = 0x36A (874)
- Calculated from region data