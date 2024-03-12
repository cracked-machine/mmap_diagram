import pytest
import typing
import mm.diagram

@pytest.fixture
def input() -> typing.Dict:
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
def zynqmp() -> typing.Dict:
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
