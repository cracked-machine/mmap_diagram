![memory map diagram](report.png)
|name|origin|size|remaining|collisions
|:-|:-|:-|:-|:-|
|<span style='color:green'>kernel</span>|0x10|0x50|-0x10|{'rootfs': '0x50'}|
|<span style='color:mediumblue'>uboot</span>|0xD0|0x50|-0x10|{'uboot-scr': '0x110'}|
|<span style='color:turquoise'>rootfs</span>|0x50|0x30|0x10|{'kernel': '0x50'}|
|<span style='color:maroon'>dtb</span>|0x90|0x30|0x10|{}|
|<span style='color:blueviolet'>uboot-scr</span>|0x110|0x30|0x50|{'uboot': '0x110'}|
