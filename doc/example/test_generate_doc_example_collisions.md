![memory map diagram](test_generate_doc_example_collisions_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:(144, 104, 152, 78)'>dtb</span>|0x90|0x30|0x328|{'rootfs': '0x90'}|
|<span style='color:(251, 144, 53, 51)'>rootfs</span>|0x50|0x50|-0x10|{'kernel': '0x50', 'dtb': '0x90'}|
|<span style='color:(85, 170, 47, 186)'>kernel</span>|0x10|0x60|-0x20|{'rootfs': '0x50'}|
