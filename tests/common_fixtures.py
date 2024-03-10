import pytest
from typing import Dict
import pathlib
import mm.diagram


@pytest.fixture
def input() -> Dict:
    valid = {
        "$schema": "../../mm/schema.json",
        "name": "TestDiagram",
        "height": mm.diagram.A8.height,
        "width": mm.diagram.A8.width,
        "memory_maps": {
            "eMMC": {
                "memory_regions": 
                {
                    "Blob1": {
                        "origin": "0x10",
                        "size": "0x10",
                    "links": [
                        ["DRAM", "Blob2"],
                        ["DRAM", "Blob3"]
                    ]
                    }
                }
            },
            "DRAM": {
                "memory_regions": 
                {
                    "Blob2": {
                        "origin": "0x10",
                        "size": "0x10"
                    },
                    "Blob3": {
                        "origin": "0x50",
                        "size": "0x10"
                    }
                }
            }
        }
    }
        
    return valid

@pytest.fixture
def zynqmp() -> Dict:
    data = {
        "$schema": "../../mm/schema.json",
        "name": "ZynqMP",
        "height": 1000,
        "width": 1000,
        "memory_maps": {
            "Global System Address Map": {
                "memory_regions": 
                {
                    "DDR Memory Controller": {
                        "origin": hex(16),
                        "size": hex(1000),
                    },
                    "OCM": {
                        "origin": hex(2016),
                        "size": hex(2000)
                    }
                }
            },
            "Flash": {
                "memory_regions":
                {
                    "Boot Image": {
                        "origin": hex(0),
                        "size": hex(2000),
                        "links": [
                            ["Global System Address Map", "OCM"]
                        ]

                    }
                }
            }
        }
    }

    return data

# @pytest.fixture
# def zynqmp_large() -> Dict:
#     data = {
#         "$schema": "../../mm/schema.json",
#         "name": "ZynqMP",
#         "height": 2480,
#         "width": 3508,
#         "memory_maps": {
#             "Global System Address Map": {
                
#                 "memory_regions": 
#                 {
#                     "DDR Memory Controller": {
#                         "origin": hex(16),
#                         "size": hex(1000),
#                     },
#                     "OCM": {
#                         "origin": hex(2016),
#                         "size": hex(2000)
#                     }
#                 }
#             },
#             "Flash": {
                
#                 "memory_regions":
#                 {
#                     "Boot Image": {
#                         "origin": hex(0),
#                         "size": "0xFFFFFF",

#                     }
#                 }
#             }
#         }
#     }

#     return data

# @pytest.fixture
# def zynqmp_max_address_exceeds_regions() -> Dict:
#     data = {
#         "$schema": "../../mm/schema.json",
#         "name": "ZynqMP",
#         "height": 2480,
#         "width": 3508,
#         "memory_maps": {
#             "Global System Address Map": {
#                 "max_address": hex(5000),
#                 "memory_regions": 
#                 {
#                     "DDR Memory Controller": {
#                         "origin": hex(16),
#                         "size": hex(1000),
#                     },
#                     "OCM": {
#                         "origin": hex(2016),
#                         "size": hex(2000)
#                     }
#                 }
#             },
#             "Flash": {
#                 "max_address": hex(5000),
#                 "memory_regions":
#                 {
#                     "Boot Image": {
#                         "origin": hex(0),
#                         "size": hex(2000),

#                     }
#                 }
#             }
#         }
#     }

#     return data


@pytest.fixture
def file_setup(request):

    report = pathlib.Path(f"{request.param['file_path']}.md")
    report.unlink(missing_ok=True)

    diagram_image = pathlib.Path(f"{request.param['file_path']}_diagram.png")
    diagram_image.unlink(missing_ok=True)

    table_image = pathlib.Path(f"{request.param['file_path']}_table.png")
    table_image.unlink(missing_ok=True)

    return {"report": report, "diagram_image": diagram_image, "table_image": table_image}


