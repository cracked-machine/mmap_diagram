![memory map diagram](tests.test_docs_three_maps_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:olive'>Blob4</span>|0x10|0x150|-0x40|{'Blob5': '0x120'}|
|<span style='color:slateblue'>Blob5</span>|0x120|0x70|0x258|{'Blob4': '0x120'}|
|<span style='color:gray'>Blob2</span>|0x10|0x10|0x30|{}|
|<span style='color:lightskyblue'>Blob3</span>|0x50|0x10|0x388|{}|
|<span style='color:limegreen'>Blob1</span>|0x10|0x10|0x3c8|{}|
