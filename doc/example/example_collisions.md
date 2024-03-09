![memory map diagram](example_collisions_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Untitled|<span style='color:(48, 45, 63)'>dtb</span>|0x90 (144)|0x30 (48)|0x328 (808)| rootfs @ 0x90 ||1:1|
|Untitled|<span style='color:(56, 63, 44)'>rootfs</span>|0x50 (80)|0x50 (80)|-0x10 (-16)| kernel @ 0x50 <BR> dtb @ 0x90 ||1:1|
|Untitled|<span style='color:(51, 4, 5)'>kernel</span>|0x10 (16)|0x60 (96)|-0x20 (-32)| rootfs @ 0x50 ||1:1|
