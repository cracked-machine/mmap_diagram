
import unittest
import mm.diagram
import mm.metamodel
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input, file_setup, zynqmp
import json
import logging


# A3
            
@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A3_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A3_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A3 size diagram, but region exceeds that height. 
        Output should remain at A3 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A3.width
    zynqmp['height'] = mm.diagram.A3.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A3_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == 4961
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 1
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == 4961
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 3382

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A3.width, mm.diagram.A3.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A3_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A3_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A3.width
    zynqmp['height'] = mm.diagram.A3.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A3_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 1
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 3544
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A3.width, mm.diagram.A3.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A3_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A3_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A3.width
    zynqmp['height'] = mm.diagram.A3.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A3_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == 4961
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 1
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 2        

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A3.width, mm.diagram.A3.height)

# A4
            
@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A4_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A4_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A4 size diagram, but region exceeds that height. 
        Output should remain at A4 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A4.width
    zynqmp['height'] = mm.diagram.A4.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A4_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == mm.diagram.A4.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 2
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == mm.diagram.A4.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 4783

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A4.width, mm.diagram.A4.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A4_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A4_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A4.width
    zynqmp['height'] = mm.diagram.A4.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A4_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 2
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 5011
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A4.width, mm.diagram.A4.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A4_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A4_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A4.width
    zynqmp['height'] = mm.diagram.A4.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A4_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == mm.diagram.A4.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 2
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 2            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A4.width, mm.diagram.A4.height)

# A5 
            

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A5_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A5_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A5 size diagram, but region exceeds that height. 
        Output should remain at A5 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A5.width
    zynqmp['height'] = mm.diagram.A5.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A5_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == mm.diagram.A5.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 2
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == mm.diagram.A5.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 6766

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A5.width, mm.diagram.A5.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A5_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A5_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A5.width
    zynqmp['height'] = mm.diagram.A5.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A5_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 2
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 7088
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A5.width, mm.diagram.A5.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A5_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A5_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A5.width
    zynqmp['height'] = mm.diagram.A5.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A5_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == mm.diagram.A5.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 2
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 3           

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A5.width, mm.diagram.A5.height)

# A6 
            
@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A6_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A6_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A6 size diagram, but region exceeds that height. 
        Output should remain at A6 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A6.width
    zynqmp['height'] = mm.diagram.A6.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A6_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == mm.diagram.A6.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 3
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == mm.diagram.A6.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 9598

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A6.width, mm.diagram.A6.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A6_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A6_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A6.width
    zynqmp['height'] = mm.diagram.A6.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A6_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 3
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 10056
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A6.width, mm.diagram.A6.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A6_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A6_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A6.width
    zynqmp['height'] = mm.diagram.A6.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A6_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == mm.diagram.A6.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 3
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 3           

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A6.width, mm.diagram.A6.height)

# A7
            
@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A7_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A7_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A7 size diagram, but region exceeds that height. 
        Output should remain at A7 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A7.width
    zynqmp['height'] = mm.diagram.A7.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A7_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == mm.diagram.A7.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 4
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == mm.diagram.A7.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 13531

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A7.width, mm.diagram.A7.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A7_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A7_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A7.width
    zynqmp['height'] = mm.diagram.A7.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A7_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 4
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 14176
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A7.width, mm.diagram.A7.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A7_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A7_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A7.width
    zynqmp['height'] = mm.diagram.A7.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A7_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == mm.diagram.A7.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 4
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 5          

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A7.width, mm.diagram.A7.height)

# A8  

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A8_region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_A8_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A8 size diagram, but region exceeds that height. 
        Output should remain at A8 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   Since the max_address was not set it was taken from the diagram height, which means the region collided with the max_address"""
    
    zynqmp['width'] = mm.diagram.A8.width
    zynqmp['height'] = mm.diagram.A8.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A8_region_exceeds_height-no_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == mm.diagram.A8.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 5
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == mm.diagram.A8.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == 19196

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A8.width, mm.diagram.A8.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A8_region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_A8_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
        NOTE: draw_scale is adjusted to allow for potential voidregions
    """
    
    zynqmp['width'] = mm.diagram.A8.width
    zynqmp['height'] = mm.diagram.A8.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/A8_region_freespace_exceeds_height-higher_maxaddress_set.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    assert mmap.draw_scale == 5
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 20112
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A8.width, mm.diagram.A8.height)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/A8_maxaddress_lower_than_memregions"}], indirect=True)
def test_generate_doc_A8_maxaddress_lower_than_memregions(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
        - 'max_address is now set below the memregions but this will be overridden with the 
        calculated largest value from the region data.
    """
    
    zynqmp['width'] = mm.diagram.A8.width
    zynqmp['height'] = mm.diagram.A8.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    input_file = pathlib.Path("./doc/example/A8_maxaddress_lower_than_memregions.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--threshold", hex(100),
                "-v"
            ],
        ):
        with caplog.at_level(logging.WARNING):

            d = mm.diagram.Diagram()

            # assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == mm.diagram.A8.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == 5
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 6          

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A8.width, mm.diagram.A8.height)
