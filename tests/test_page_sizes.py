
import unittest
import mm.diagram
import mm.metamodel
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import zynqmp, file_setup
import json
import logging


test_desc = """ 
-   region exceeds diagram height. 
    Output should remain at page size but the drawing ratio will adjust to fit the larger contents
    Note the ratio is rounded up to nearest integer value.
-   Since the max_address was not set it was taken from the diagram height, 
    which means the region collided with the max_address
"""

@pytest.mark.parametrize(
    'psize, expected_scale_res, file_setup', 
    [
        (mm.diagram.A3, (1, 3382), {"file_path": "docs/example/A3_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A4, (2, 4783), {"file_path": "docs/example/A4_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A5, (2, 6766), {"file_path": "docs/example/A5_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A6, (3, 9598), {"file_path": "docs/example/A6_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A7, (4, 13531), {"file_path": "docs/example/A7_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A8, (5, 19196), {"file_path": "docs/example/A8_region_exceeds_height_no_maxaddress_set", "test_desc": test_desc}),
    ], indirect=['file_setup']
)
def test_generate_doc_region_exceeds_height_no_maxaddress_set(
    zynqmp,
    expected_scale_res,
    psize,
    file_setup,
    
):

    # test data setup
    zynqmp['width'] = psize.width
    zynqmp['height'] = psize.height

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    with file_setup['json_file'].open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    # test start
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(file_setup['json_file']),
                "--out", str(file_setup['report']),
                "--threshold", hex(100)
            ],
        ):

        d = mm.diagram.Diagram()
        mmap: mm.metamodel.MemoryMap
        for mname, mmap in d.model.memory_maps.items():
            if mname == 'Global System Address Map':
                # "DDR Memory Controller" origin + size + "OCM" size
                assert mmap.max_address == psize.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == expected_scale_res[0]
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == psize.height
                assert mmap.max_address_taken_from_diagram_height == True
                assert mmap.draw_scale == expected_scale_res[1]

        assert file_setup['diagram_image'].exists()
        assert PIL.Image.open( str(file_setup['diagram_image']) ).size == (
            psize.width, 
            psize.height)


test_desc = """ 
            -   'max_address' is now set at a higher value than the max region size. 
                This will cause excessive freespace values to be created (larger than the diagram height).
                To prevent illegible diagrams, the pre-calculated value will be used instead.
                NOTE: draw_scale is adjusted to allow for potential voidregions
            """
@pytest.mark.parametrize(
    'psize, expected_scale_res, file_setup', 
    [
        (mm.diagram.A3, (1, 3544), {"file_path": "docs/example/A3_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A4, (2, 5011), {"file_path": "docs/example/A4_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A5, (2, 7088), {"file_path": "docs/example/A5_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A6, (3, 10056), {"file_path": "docs/example/A6_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A7, (4, 14176), {"file_path": "docs/example/A7_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
        (mm.diagram.A8, (5, 20112), {"file_path": "docs/example/A8_region_freespace_exceeds_height_higher_maxaddress_set", "test_desc": test_desc}),
    ], indirect=['file_setup']
)
def test_generate_doc_region_freespace_exceeds_height_higher_maxaddress_set(
    zynqmp,
    expected_scale_res,
    psize,
    file_setup,
    caplog,
    
):
    zynqmp['width'] = psize.width
    zynqmp['height'] = psize.height

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    with file_setup['json_file'].open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(file_setup['json_file']),
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
                    assert mmap.draw_scale == expected_scale_res[0]
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == expected_scale_res[1]
            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (psize.width, psize.height)


test_desc = """ 
                - 'max_address is now set below the memregions but this will be overridden with the 
                calculated largest value from the region data.
            """
@pytest.mark.parametrize(
    'psize, expected_scale_res, file_setup', 
    [
        (mm.diagram.A3, (1, 2), {"file_path": "docs/example/A3_maxaddress_lower_than_memregions", "test_desc": test_desc}),
        (mm.diagram.A4, (2, 2), {"file_path": "docs/example/A4_maxaddress_lower_than_memregions", "test_desc": test_desc}),
        (mm.diagram.A5, (2, 3), {"file_path": "docs/example/A5_maxaddress_lower_than_memregions", "test_desc": test_desc}),
        (mm.diagram.A6, (3, 3), {"file_path": "docs/example/A6_maxaddress_lower_than_memregions", "test_desc": test_desc}),
        (mm.diagram.A7, (4, 5), {"file_path": "docs/example/A7_maxaddress_lower_than_memregions", "test_desc": test_desc}),
        (mm.diagram.A8, (5, 6), {"file_path": "docs/example/A8_maxaddress_lower_than_memregions", "test_desc": test_desc}),
    ], indirect=['file_setup']
)
def test_generate_doc_maxaddress_lower_than_memregions(
    zynqmp,
    expected_scale_res,
    psize,
    file_setup,
    caplog,
    
):
    zynqmp['width'] = psize.width
    zynqmp['height'] = psize.height

    zynqmp['link_head_width'] = 100 # who doesn't like a giant arrow?

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['origin'] = hex(3000)
    new_max_address = 2000
    zynqmp['memory_maps']['Flash']['max_address'] = hex(new_max_address)
    # zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    with file_setup['json_file'].open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(file_setup['json_file']),
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
                    assert mmap.max_address == psize.height
                    assert mmap.max_address_taken_from_diagram_height == True
                    assert mmap.draw_scale == expected_scale_res[0]
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == new_max_address
                    assert mmap.max_address_taken_from_diagram_height == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == expected_scale_res[1]

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (psize.width, psize.height)
