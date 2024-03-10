![memory map diagram](example_collisions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(37, 66, 23)'>dtb (Untitled)</span>|0x90 (144)|0x30 (48)|0x2aa (682)| rootfs @ 0x90 ||1:1|
|<span style='color:(1, 28, 14)'>rootfs (Untitled)</span>|0x50 (80)|0x50 (80)|-0x10 (-16)| kernel @ 0x50 <BR> dtb @ 0x90 ||1:1|
|<span style='color:(29, 12, 45)'>kernel (Untitled)</span>|0x10 (16)|0x60 (96)|-0x20 (-32)| rootfs @ 0x50 ||1:1|

---
#### Untitled:
- max address = 0x36A (874)
- User-defined input