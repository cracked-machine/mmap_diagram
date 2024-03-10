![memory map diagram](example_end_collision_diagram.png)
|region (parent)|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|
|<span style='color:(34, 9, 20)'>dtb (Untitled)</span>|0x190 (400)|0x30 (48)|-0xb (-11)| end @ 0x1b5 ||2:1|
|<span style='color:(35, 14, 37)'>rootfs (Untitled)</span>|0x50 (80)|0x30 (48)|0x110 (272)|||2:1|
|<span style='color:(24, 40, 51)'>kernel (Untitled)</span>|0x10 (16)|0x30 (48)|0x10 (16)|||2:1|

---
#### Untitled:
- max address = 0x1B5 (437)
- User-defined input