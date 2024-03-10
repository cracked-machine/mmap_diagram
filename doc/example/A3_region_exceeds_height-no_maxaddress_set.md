![memory map diagram](A3_region_exceeds_height-no_maxaddress_set_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(15, 3, 54)'>OCM (Global System Address Map)</span>|0x7e0 (2016)|0x7d0 (2000)|0x3b1 (945)|||1:1|
|<span style='color:(2, 18, 1)'>DDR Memory Controller (Global System Address Map)</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||1:1|
|<span style='color:(34, 42, 50)'>Boot Image (Flash)</span>|0x0 (0)|0xffffff (16777215)|-0xffec9e (-16772254)| end @ 0x1361 ||3382:1|

---
#### Global System Address Map:
- max address = 0x1361 (4,961)
- Calculated from region data
#### Flash:
- max address = 0x1361 (4,961)
- Calculated from region data