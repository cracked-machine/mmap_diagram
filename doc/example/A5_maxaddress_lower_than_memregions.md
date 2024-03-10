![memory map diagram](A5_maxaddress_lower_than_memregions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(52, 49, 16)'>Boot Image (Flash)</span>|0xbb8 (3000)|0x7d0 (2000)|0x0 (0)||('Global System Address Map', 'OCM')|3:1|
|<span style='color:(4, 9, 30)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||2:1|
|<span style='color:(53, 59, 26)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||2:1|

---
#### Global System Address Map:
- max address = 0xFB0 (4,016)
- Calculated from region data
#### Flash:
- max address = 0x1388 (5,000)
- Calculated from region data