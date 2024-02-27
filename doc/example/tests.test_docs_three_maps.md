![memory map diagram](tests.test_docs_three_maps_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:(205, 46, 148, 14)'>Blob6</span>|0x50|0x96|0x302|{'Blob5': '0x50'}|
|<span style='color:(193, 106, 92, 43)'>Blob3</span>|0x50|0x10|0x388|{}|
|<span style='color:(83, 162, 66, 115)'>Blob5</span>|0x32|0x64|-0x46|{'Blob4': '0x32', 'Blob6': '0x50'}|
|<span style='color:(103, 4, 7, 15)'>Blob2</span>|0x10|0x10|0x30|{}|
|<span style='color:(170, 220, 232, 76)'>Blob1</span>|0x10|0x10|0x3c8|{}|
|<span style='color:(89, 118, 29, 192)'>Blob4</span>|0xa|0x3c|-0x14|{'Blob5': '0x32'}|
