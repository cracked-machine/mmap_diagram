![memory map diagram](test_generate_doc_example_collisions_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|Untitled|<span style='color:(50, 27, 41)'>dtb</span>|0x90|0x30|0x328| rootfs @ 0x90 ||
|Untitled|<span style='color:(3, 58, 68)'>rootfs</span>|0x50|0x50|-0x10| kernel @ 0x50 <BR> dtb @ 0x90 ||
|Untitled|<span style='color:(63, 56, 45)'>kernel</span>|0x10|0x60|-0x20| rootfs @ 0x50 ||
