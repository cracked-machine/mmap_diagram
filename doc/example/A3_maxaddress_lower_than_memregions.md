![memory map diagram](A3_maxaddress_lower_than_memregions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(35, 1, 13)'>Boot Image (Flash)</span>|0xbb8 (3000)|0x7d0 (2000)|-0xbb8 (-3000)| end @ 0x7d0 |('Global System Address Map', 'OCM')|2:1|
|<span style='color:(10, 56, 26)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x3b1 (945)|||1:1|
|<span style='color:(7, 14, 5)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|

---
#### Global System Address Map:
- max address = 0x1361 (4,961)
- Calculated from region data
#### Flash:
- max address = 0x7D0 (2,000)
- User-defined input