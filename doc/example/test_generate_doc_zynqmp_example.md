![memory map diagram](test_generate_doc_zynqmp_example_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(7, 38, 29)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x0 (0)|||5:1|
|Global System Address Map|<span style='color:(47, 30, 55)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||5:1|
|Flash|<span style='color:(13, 10, 32)'>Boot Image</span>|0x0 (0)|0x7d0 (2000)|0x0 (0)||('Global System Address Map', 'OCM')|2:1|
