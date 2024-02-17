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
        "$schema": "/home/chris/projects/python/mmdiagram/mm/schema.json",
        "diagram_name": "TestDiagram",
        "memory_maps": {
            "eMMC": {
                "memory_regions": 
                {
                    "Blob1": {
                    "memory_region_origin": "0x10",
                    "memory_region_size": "0x10",
                    "memory_region_links": [
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
                    "memory_region_origin": "0x10",
                    "memory_region_size": "0x10"
                    },
                    "Blob3": {
                    "memory_region_origin": "0x50",
                    "memory_region_size": "0x10"
                    }
                }
            }
        }
    }
        
    return valid
    
def test_schema_gen(setup):
    mm.schema.generate_schema(setup["schema"])
    assert setup["schema"].exists()

def test_gen_example_input(input):
    data = mm.schema.Diagram(**input)

    output_file = pathlib.Path("./doc/example/input.json")
    with output_file.open("w") as fp:
        fp.write(data.model_dump_json(indent=2))
    
    assert output_file.exists()
    
def test_data_present(input):
    data = mm.schema.Diagram(**input)
    # check there is data present
    assert data.memory_maps['eMMC'].memory_regions['Blob1']
    assert data.memory_maps['DRAM'].memory_regions['Blob2']
    assert data.memory_maps['DRAM'].memory_regions['Blob3']
    

def test_schema_missing_diagram_name(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['diagram_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_memregion_origin_emptystr(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_origin'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_size(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_hexstr_memregion_origin(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_origin'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_hexstr_memregion_size(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_memregion_links(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)
    
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["NotExist","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["DRAM",""]
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["DRAM","NotExist"]
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)


def test_schema_memregion_links_mismatched_sizes(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - eMMC:Blob1 is linked to DRAM:Blob2 and now they are different sizes - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = "0x10"
    test_data['memory_maps']['DRAM']['memory_regions']['Blob2']['memory_region_size'] = "0x20"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)       


