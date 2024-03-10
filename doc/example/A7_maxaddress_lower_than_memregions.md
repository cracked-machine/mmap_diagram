![memory map diagram](A7_maxaddress_lower_than_memregions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(6, 34, 3)'>Boot Image (Flash)</span>|0xbb8 (3000)|0x7d0 (2000)|-0xbb8 (-3000)| end @ 0x7d0 |('Global System Address Map', 'OCM')|5:1|
|<span style='color:(55, 66, 20)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|-0xad8 (-2776)| end @ 0x4d8 ||4:1|
|<span style='color:(63, 55, 51)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||4:1|

---
#### Global System Address Map:
- max address = 0x4D8 (1,240)
- Calculated from region data
#### Flash:
- max address = 0x7D0 (2,000)
- User-defined input