![memory map diagram](A6_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(23, 62, 48)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0x8dc (-2268)| end @ 0x6d4 ||3:1|
|<span style='color:(41, 30, 68)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||3:1|
|<span style='color:(7, 45, 51)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xfff92b (-16775467)| end @ 0x6d4 ||9598:1|

---
#### Global System Address Map:
- max address = 0x6D4 (1,748)
- Calculated from region data
#### Flash:
- max address = 0x6D4 (1,748)
- Calculated from region data