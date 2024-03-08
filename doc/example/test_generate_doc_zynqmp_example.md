![memory map diagram](test_generate_doc_zynqmp_example_redux.png)
|map|region|origin|size|free Space|collisions|links|draw scale|
|:-|:-|:-|:-|:-|:-|:-|:-|
|Global System Address Map|<span style='color:(2, 55, 67)'>OCM</span>|0x7e0 (2016)|0x7d0 (2000)|0x1d8 (472)|||2:1|
|Global System Address Map|<span style='color:(52, 38, 3)'>DDR Memory Controller</span>|0x10 (16)|0x3e8 (1000)|0x3e8 (1000)|||2:1|
|Flash|<span style='color:(51, 15, 51)'>Boot Image</span>|0x0 (0)|0x7d0 (2000)|0x1e0 (480)||('Global System Address Map', 'OCM')|1:1|
