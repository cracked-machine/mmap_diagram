![memory map diagram](tests.test_docs_collisions.png)
|name|origin|size|remaining|collisions
|:-|:-|:-|:-|:-|
|<span style='color:darkslateblue'>kernel</span>|0x10|0x60|-0x20|{'rootfs': '0x50'}|
|<span style='color:gray'>rootfs</span>|0x50|0x50|-0x10|{'kernel': '0x50', 'dtb': '0x90'}|
|<span style='color:limegreen'>dtb</span>|0x90|0x30|0x328|{'rootfs': '0x90'}|
