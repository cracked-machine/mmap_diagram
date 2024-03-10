![memory map diagram](example_region_collisions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(26, 31, 43)'>dtb (Untitled)</span>|0x90 (144)|0x30 (48)|0xf5 (245)| rootfs @ 0x90 ||1:1|
|<span style='color:(13, 5, 17)'>rootfs (Untitled)</span>|0x50 (80)|0x50 (80)|-0x10 (-16)| kernel @ 0x50 <BR> dtb @ 0x90 ||1:1|
|<span style='color:(28, 54, 24)'>kernel (Untitled)</span>|0x10 (16)|0x60 (96)|-0x20 (-32)| rootfs @ 0x50 ||1:1|

---
#### Untitled:
- max address = 0x1B5 (437)
- User-defined input