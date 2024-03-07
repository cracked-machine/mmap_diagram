![memory map diagram](test_generate_doc_example_collisions_redux.png)
|map|region|origin|size|free Space|collisions|links|
|:-|:-|:-|:-|:-|:-|:-|
|Untitled|<span style='color:(27, 44, 22)'>dtb</span>|0x90|0x30|0x328| rootfs @ 0x90 ||
|Untitled|<span style='color:(7, 15, 27)'>rootfs</span>|0x50|0x50|-0x10| kernel @ 0x50 <BR> dtb @ 0x90 ||
|Untitled|<span style='color:(25, 62, 63)'>kernel</span>|0x10|0x60|-0x20| rootfs @ 0x50 ||
