![memory map diagram](example_collisions_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(51, 0, 40)'>dtb (Untitled)</span>|0x90 (144)|0x30 (48)|0x328 (808)| rootfs @ 0x90 ||1:1|
|<span style='color:(37, 6, 9)'>rootfs (Untitled)</span>|0x50 (80)|0x50 (80)|-0x10 (-16)| kernel @ 0x50 <BR> dtb @ 0x90 ||1:1|
|<span style='color:(54, 29, 58)'>kernel (Untitled)</span>|0x10 (16)|0x60 (96)|-0x20 (-32)| rootfs @ 0x50 ||1:1|

---
#### Untitled:
- max address = 0x3E8 (1,000)
- User-defined input