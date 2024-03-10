![memory map diagram](A5_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(16, 30, 65)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0x600 (-1536)| end @ 0x9b0 ||2:1|
|<span style='color:(62, 31, 16)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||2:1|
|<span style='color:(26, 18, 17)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xfff64f (-16774735)| end @ 0x9b0 ||6766:1|

---
#### Global System Address Map:
- max address = 0x9B0 (2,480)
- Calculated from region data
#### Flash:
- max address = 0x9B0 (2,480)
- Calculated from region data