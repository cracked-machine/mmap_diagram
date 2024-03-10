![memory map diagram](A8_maxaddress_lower_than_memregions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(66, 0, 56)'>Boot Image (Flash)</span>|0xbb8 (3000)|0x7d0 (2000)|-0xbb8 (-3000)| end @ 0x7d0 |('Global System Address Map', 'OCM')|6:1|
|<span style='color:(13, 23, 40)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0xc46 (-3142)| end @ 0x36a ||5:1|
|<span style='color:(62, 27, 1)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|-0x8e (-142)| end @ 0x36a ||5:1|

---
#### Global System Address Map:
- max address = 0x36A (874)
- Calculated from region data
#### Flash:
- max address = 0x7D0 (2,000)
- User-defined input