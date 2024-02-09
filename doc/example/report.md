![memory map diagram](report.png)
|name|origin|size|remaining|collisions
|:-|:-|:-|:-|:-|
|<span style='color:mediumaquamarine'>kernel</span>|0x10|0x50|-0x10|{'rootfs': '0x50'}|
|<span style='color:chartreuse'>uboot</span>|0xD0|0x50|-0x10|{'uboot-scr': '0x110'}|
|<span style='color:skyblue'>rootfs</span>|0x50|0x30|0x10|{'kernel': '0x50'}|
|<span style='color:lightgreen'>dtb</span>|0x90|0x30|0x10|{}|
|<span style='color:grey'>uboot-scr</span>|0x110|0x30|0x50|{'uboot': '0x110'}|
