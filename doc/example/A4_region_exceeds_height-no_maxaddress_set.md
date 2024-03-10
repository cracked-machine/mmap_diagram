![memory map diagram](A4_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(63, 63, 33)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0x1fc (-508)| end @ 0xdb4 ||2:1|
|<span style='color:(2, 12, 11)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||2:1|
|<span style='color:(65, 47, 51)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xfff24b (-16773707)| end @ 0xdb4 ||4783:1|

---
#### Global System Address Map:
- max address = 0xDB4 (3,508)
- Calculated from region data
#### Flash:
- max address = 0xDB4 (3,508)
- Calculated from region data