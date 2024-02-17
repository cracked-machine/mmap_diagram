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
                    },
                    {
                        "memory_region_name": "Blob3",
                        "memory_region_origin": "0x50",
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

def test_gen_example_input(input):
    data = mm.schema.Diagram(**input)

    output_file = pathlib.Path("./doc/example/input.json")
    with output_file.open("w") as fp:
        fp.write(data.model_dump_json(indent=2))
    
    assert output_file.exists()
    
def test_data_present(input):
    data = mm.schema.Diagram(**input)
    # check there is data present
    assert data.memory_maps
    assert len(data.memory_maps) == 2
    for memmap in data.memory_maps:
        assert memmap.memory_regions

def test_schema_valid_example(input):
    test_data = input
    mm.schema.Diagram(**test_data)

def test_schema_missing_diagram_name(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['diagram_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memmap_name(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    d = mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_map_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_name(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_origin(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_origin'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_missing_memregion_size(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_size'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_hexstr_memregion_origin(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_origin'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_hexstr_memregion_size(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_size'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

def test_schema_memregion_links(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_links'][0] = { "": "Blob2"}
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)
    
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_links'][0] = { "Nothing": "Blob2"}
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_links'][0] = { "DRAM": ""}
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)

    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_links'][0] = { "DRAM": "Nothing"}
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)


def test_schema_memregion_links_mismatched_sizes(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps'][0]['memory_regions'][0]['memory_region_size'] = "0x20"
    with pytest.raises(pydantic.ValidationError): 
        mm.schema.Diagram(**test_data)       

def test_schema_duplicate_region_names_within_same_mmap(input):
    test_data = input

    # default test_data contains non-empty string - should pass
    mm.schema.Diagram(**test_data)

    # invalidate test_data by setting duplicate names in the second mmap regions - should fail
    # test_data['memory_maps'][1]['memory_regions'][0]['memory_region_name'] = "blob2"
    # mmdut = [mm for mm in test_data['memory_maps'] if mm['memory_map_name'] == "DRAM"]  

    mm.schema.find_memregion_by_name("DRAM", "Blob2", test_data)['memory_region_name'] = "Blob2"
    mm.schema.find_memregion_by_name("DRAM", "Blob3", test_data)['memory_region_name'] = "Blob2"
    
    
    with pytest.raises(pydantic.ValidationError): 
        d = mm.schema.Diagram(**test_data)  
        