![memory map diagram](tests.test_docs_three_maps_cropped.png)
|name|origin|size|free Space|collisions
|:-|:-|:-|:-|:-|
|<span style='color:chartreuse'>Blob6</span>|0x50|0x96|0x302|{'Blob5': '0x50'}|
|<span style='color:darkslategrey'>Blob3</span>|0x50|0x10|0x388|{}|
|<span style='color:olivedrab'>Blob5</span>|0x32|0x64|-0x46|{'Blob4': '0x32', 'Blob6': '0x50'}|
|<span style='color:darkred'>Blob2</span>|0x10|0x10|0x30|{}|
|<span style='color:mediumblue'>Blob1</span>|0x10|0x10|0x3c8|{}|
|<span style='color:olive'>Blob4</span>|0xa|0x3c|-0x14|{'Blob5': '0x32'}|
