![memory map diagram](test_generate_doc_example_collisions_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:(41, 28, 31)'>dtb</span>|0x90|0x30|0x328|{'rootfs': '0x90'}|
|<span style='color:(57, 41, 29)'>rootfs</span>|0x50|0x50|-0x10|{'kernel': '0x50', 'dtb': '0x90'}|
|<span style='color:(45, 65, 13)'>kernel</span>|0x10|0x60|-0x20|{'rootfs': '0x50'}|
