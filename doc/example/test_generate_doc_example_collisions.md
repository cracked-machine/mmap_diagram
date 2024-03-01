![memory map diagram](test_generate_doc_example_collisions_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:(129, 9, 221, 0)'>dtb</span>|0x90|0x30|0x328|{'rootfs': '0x90'}|
|<span style='color:(75, 183, 142, 168)'>rootfs</span>|0x50|0x50|-0x10|{'kernel': '0x50', 'dtb': '0x90'}|
|<span style='color:(40, 135, 61, 205)'>kernel</span>|0x10|0x60|-0x20|{'rootfs': '0x50'}|
