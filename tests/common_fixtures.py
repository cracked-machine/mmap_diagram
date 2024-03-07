import pytest
from typing import Dict
import pathlib

@pytest.fixture
def input() -> Dict:
    valid = {
        "$schema": "../mm/schema.json",
        "name": "TestDiagram",
        "height": 1000,
        "width": 1000,
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
        "$schema": "../mm/schema.json",
        "name": "ZynqMP",
        "height": 1000,
        "width": 1000,
        "memory_maps": {
            "GlobalSystemAddressMap": {
                "memory_regions": 
                {
                    "DDRMemoryController": {
                        "origin": "0x10",
                        "size": hex(2000),
       
                    }
                }
            },
            # "DRAM": {
            #     "memory_regions": 
            #     {
            #         "Blob2": {
            #             "origin": "0x10",
            #             "size": "0x10"
            #         },
            #         "Blob3": {
            #             "origin": "0x50",
            #             "size": "0x10"
            #         }
            #     }
            # }
        }
    }

    return data

@pytest.fixture
def file_setup(request):

    report = pathlib.Path(f"{request.param['file_path']}.md")
    report.unlink(missing_ok=True)

    diagram_image = pathlib.Path(f"{request.param['file_path']}_redux.png")
    diagram_image.unlink(missing_ok=True)

    table_image = pathlib.Path(f"{request.param['file_path']}_table.png")
    table_image.unlink(missing_ok=True)

    return {"report": report, "diagram_image": diagram_image, "table_image": table_image}


