![memory map diagram](report.png)
|name|origin|size|remaining|collisions
|:-|:-|:-|:-|:-|
|<span style='color:midnightblue'>dtb</span>|0x90|0x100|0x258|{}|
|<span style='color:aqua'>kernel</span>|0x10|0x60|0x0|{}|
|<span style='color:lime'>rootfs</span>|0x70|0x10|0x10|{'kernel': '0x70'}|
