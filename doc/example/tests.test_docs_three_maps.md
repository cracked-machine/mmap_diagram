![memory map diagram](tests.test_docs_three_maps_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:lightseagreen'>Blob4</span>|0xa|0x3c|-0x14|{'Blob5': '0x32'}|
|<span style='color:seagreen'>Blob5</span>|0x32|0x64|-0x46|{'Blob4': '0x32', 'Blob6': '0x50'}|
|<span style='color:springgreen'>Blob6</span>|0x50|0x96|0x302|{'Blob5': '0x50'}|
|<span style='color:grey'>Blob2</span>|0x10|0x10|0x30|{}|
|<span style='color:lime'>Blob3</span>|0x50|0x10|0x388|{}|
|<span style='color:darkcyan'>Blob1</span>|0x10|0x10|0x3c8|{}|
