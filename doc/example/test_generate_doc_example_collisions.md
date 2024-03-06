![memory map diagram](test_generate_doc_example_collisions_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|Untitled|<span style='color:(8, 66, 68)'>dtb</span>|0x90|0x30|0x328| rootfs @ 0x90 ||
|Untitled|<span style='color:(44, 58, 12)'>rootfs</span>|0x50|0x50|-0x10| kernel @ 0x50 <BR> dtb @ 0x90 ||
|Untitled|<span style='color:(23, 1, 28)'>kernel</span>|0x10|0x60|-0x20| rootfs @ 0x50 ||
