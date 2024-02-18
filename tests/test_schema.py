import pytest
import pathlib
import mm.metamodel
import pydantic 
from typing import Dict
from tests.common_fixtures import input


@pytest.fixture
def setup() -> Dict:
    schema = pathlib.Path("./mm/schema.json")
    schema.unlink(missing_ok=True)
    return {"schema": schema}


def test_schema_gen(setup):
    mm.metamodel.generate_schema(setup["schema"])
    assert setup["schema"].exists()

def test_gen_example_input(input):
    data = mm.metamodel.Diagram(**input)

    output_file = pathlib.Path("./doc/example/input.json")
    with output_file.open("w") as fp:
        fp.write(data.model_dump_json(indent=2))
    
    assert output_file.exists()
    
def test_data_present(input):
    data = mm.metamodel.Diagram(**input)
    # check there is data present
    assert data.memory_maps['eMMC'].memory_regions['Blob1']
    assert data.memory_maps['DRAM'].memory_regions['Blob2']
    assert data.memory_maps['DRAM'].memory_regions['Blob3']
    

def test_schema_missing_diagram_name(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['diagram_name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_memregion_origin_emptystr(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_origin'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_missing_memregion_size(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_hexstr_memregion_origin(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_origin'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_hexstr_memregion_size(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_memregion_links(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)
    
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["NotExist","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["DRAM",""]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_links'][0] = ["DRAM","NotExist"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)


def test_schema_memregion_links_mismatched_sizes(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - eMMC:Blob1 is linked to DRAM:Blob2 and now they are different sizes - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['memory_region_size'] = "0x10"
    test_data['memory_maps']['DRAM']['memory_regions']['Blob2']['memory_region_size'] = "0x20"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)       


