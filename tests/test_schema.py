import pytest
import pathlib
import mm.metamodel
import pydantic 
from typing import Dict
from tests.common_fixtures import input
import unittest
import logging

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

    output_file = pathlib.Path("./docs/example/input.json")
    with output_file.open("w") as fp:
        fp.write(data.model_dump_json(indent=2))
    
    assert output_file.exists()

def test_input_file(caplog):

    # Check you get warning with -f and -l
    with unittest.mock.patch(
        "sys.argv", 
        [
            "mm.diagram", 
            "-f", "input.json",
            "-l", hex(1000),
            "-t", hex(500)
        ]
    ):        
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()
            
    caplog.clear()

    # Check you get warning with -f and -l
    with unittest.mock.patch(
        "sys.argv", 
        [
            "mm.diagram", 
            "-f", "docs/example/input.json",
            "-l", hex(1000),
            "-t", hex(500)
        ]
    ):        
        with caplog.at_level(logging.WARNING):
            d = mm.diagram.Diagram()
            assert 'Limit flag is ignore when using JSON input. Using the JSON file Diagram -> height field instead.' in caplog.text

    caplog.clear()

        # Check you get don't get warning with only -l
    with unittest.mock.patch(
        "sys.argv", 
        [
            "mm.diagram", 
            "a", "0x10", "0x10",
            "-l", hex(1000),
            "-t", hex(500)
        ]
    ):

        with caplog.at_level(logging.WARNING):
            d = mm.diagram.Diagram()
            assert not 'Limit flag is ignore when using JSON input. Using the JSON file Diagram -> height field instead.' in caplog.text
    
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
    test_data['name'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_memregion_origin_emptystr(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['origin'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_missing_memregion_size(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['size'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_region_alpha_limits(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['region_alpha'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['region_alpha'] = 256
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['region_alpha'] = -1
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_link_alpha_limits(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)

    # invalidate test_data - should fail
    test_data['link_alpha'] = ""
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['link_alpha'] = 256
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['link_alpha'] = -1
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_hexstr_memregion_origin(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['origin'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_hexstr_memregion_size(input):
    test_data = input
    
    # default test_data contains hex string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['size'] = "10"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

def test_schema_memregion_links(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['links'][0] = ["","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)
    
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['links'][0] = ["NotExist","Blob2"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['links'][0] = ["DRAM",""]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)

    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['links'][0] = ["DRAM","NotExist"]
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)


def test_schema_memregion_links_mismatched_sizes(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # invalidate test_data - eMMC:Blob1 is linked to DRAM:Blob2 and now they are different sizes - should fail
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['size'] = "0x10"
    test_data['memory_maps']['DRAM']['memory_regions']['Blob2']['size'] = "0x20"
    with pytest.raises(pydantic.ValidationError): 
        mm.metamodel.Diagram(**test_data)       


def test_schema_memregion_text_size_is_respected(input):
    test_data = input
    
    # default test_data contains non-empty string - should pass
    mm.metamodel.Diagram(**test_data)
    
    # verify that user input schema overrides the default (0), should not be overwritten with diagram text size (12)
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['text_size'] = "20"
    test_data['memory_maps']['eMMC']['memory_regions']['Blob1']['address_text_size'] = "20"

    d = mm.metamodel.Diagram(**test_data)       
    for mmaps in d.memory_maps.values():
        for name, mregion in mmaps.memory_regions.items():
            if name == "Blob1":
                assert mregion.text_size == 20
                assert mregion.address_text_size == 20

