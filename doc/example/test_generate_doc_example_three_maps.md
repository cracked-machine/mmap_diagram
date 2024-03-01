![memory map diagram](test_generate_doc_example_three_maps_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:(126, 128, 80, 182)'>Blob3</span>|0x50|0x10|0x388|{}|
|<span style='color:(241, 107, 95, 148)'>Blob6</span>|0x50|0x96|0x302|{'Blob5': '0x50'}|
|<span style='color:(152, 186, 151, 102)'>Blob5</span>|0x32|0x64|-0x46|{'Blob4': '0x32', 'Blob6': '0x50'}|
|<span style='color:(126, 128, 80, 182)'>Blob1</span>|0x10|0x10|0x3c8|{}|
|<span style='color:(126, 128, 80, 182)'>Blob2</span>|0x10|0x10|0x30|{}|
|<span style='color:(3, 153, 81, 58)'>Blob4</span>|0xa|0x3c|-0x14|{'Blob5': '0x32'}|
