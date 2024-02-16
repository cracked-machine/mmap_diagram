import pytest
import pathlib
import mm.schema
import pydantic 
from typing import Dict

@pytest.fixture
def setup() -> Dict:
    schema = pathlib.Path("./mm/schema.json")
    schema.unlink(missing_ok=True)
    return {"schema": schema}

@pytest.fixture
def input() -> Dict:
    valid = {
        "$schema": "../../mm/schema.json",
        "diagram_name": "TestDiagram",
        "memory_maps": [
            {
                "memory_map_name": "eMMC",
                "memory_regions": [
                    {
                        "memory_region_name": "Blob1",
                        "memory_region_origin": "0x10",
                        "memory_region_size": "0x10",
                        "memory_region_links": [
                            {
                                "DRAM": "Blob2"
                            }
                        ]
                    }
                ]
            },
            {
                "memory_map_name": "DRAM",
                "memory_regions": [
                    {
                        "memory_region_name": "Blob2",
                        "memory_region_origin": "0x10",
                        "memory_region_size": "0x10"
                        
                    }
                ]
            }
        ]
    }
    return valid

def test_schema_gen(setup):
    mm.schema.generate_schema(setup["schema"])
    assert setup["schema"].exists()
    
def test_schema_valid_example(input):
    test_data = input
    mm.schema.Diagram(**test_data)

def test_schema_missing_diagram_name(input):
    test_data = input
    test_data['diagram_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memmap_name(input):
    test_data = input
    test_data['memory_maps'][0]['memory_map_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_name(input):
    test_data = input
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_origin(input):
    test_data = input
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_origin'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_size(input):
    test_data = input
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_size'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)