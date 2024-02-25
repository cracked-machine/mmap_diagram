![memory map diagram](tests.test_docs_collisions_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:navy'>dtb</span>|0x90|0x30|0x328|{'rootfs': '0x90'}|
|<span style='color:steelblue'>rootfs</span>|0x50|0x50|-0x10|{'kernel': '0x50', 'dtb': '0x90'}|
|<span style='color:midnightblue'>kernel</span>|0x10|0x60|-0x20|{'rootfs': '0x50'}|
