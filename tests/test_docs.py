import unittest
import mm.diagram
import mm.metamodel
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input, file_setup, zynqmp
import json
import logging


@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/example_normal"}], indirect=True)
def test_generate_doc_example_normal(file_setup):
    """ """

    height = 1000
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "--out", str(file_setup["report"]),
            "-l", hex(height),
            "--threshold", hex(200),
            "--trim_whitespace"
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x110"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x190"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x228"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (400, 288)

        # reduced void threshold, so empty section between rootfs and dtb should be voided, making the file smaller
        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/example_collisions"}], indirect=True)
def test_generate_doc_example_collisions(file_setup):
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x50",
            "dtb", "0x90", "0x30",
            "--out", str(file_setup["report"]),
            "--limit", height,
            "--threshold", hex(200),
            "--trim_whitespace"
        ],
    ):

        d =mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x60"
                assert region_image.freespace_as_hex == "-0x20"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x50"
                assert region_image.freespace_as_hex == "-0x10"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x90"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x328"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (400, 260)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/example_two_maps"}], indirect=True)
def test_generate_doc_example_two_maps(input, file_setup):
    """ """

    input['memory_maps']['eMMC']['memory_regions']['Blob4'] = {
        "origin": "0x100",
        "size": "0x10"
    }

    input['memory_maps']['DRAM']['memory_regions']['Blob5'] = {
        "origin": "0x30",
        "size": "0x10"
    }

    input_file = pathlib.Path("./doc/example/two_maps_input.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    height = 1000
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--limit", hex(height),
                "--threshold", hex(200),
                "--trim_whitespace"
            ],
        ):

        

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 130)


        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/example_three_maps"}], indirect=True)
def test_generate_doc_example_three_maps(input, file_setup):
    
    """ """
    input["memory_maps"]['eMMC']['memory_regions']['Blob1'] = {
        "origin": hex(0),
        "size": hex(32),
        "links": [
            ["DRAM", "Blob2"],
            ["DRAM", "Blob4"]
        ]
    }

    input["memory_maps"]['DRAM']['memory_regions']['Blob2'] = {
        "origin": hex(0),
        "size": hex(32),
    }
    input["memory_maps"]['DRAM']['memory_regions']['Blob3'] = {
        "origin": hex(80),
        "size": hex(32),
    }    
    input["memory_maps"]['DRAM']['memory_regions']['Blob4'] = {
        "origin": hex(40),
        "size": hex(32),
    }
    input["memory_maps"]['DRAM']['memory_regions']['Blob5'] = {
        "origin": hex(120),
        "size": hex(32),
    }
    input["memory_maps"]['flash'] = {           
        "memory_regions": 
        {
            "Blob6": {
                "origin": hex(10),
                "size": hex(60)
            },
            "Blob7": {
                "origin": hex(80),
                "size": hex(32),
                "links": [
                    ["DRAM", "Blob3"],
                    ["DRAM", "Blob5"]
                ]
            }
        }        
    }

    input_file = pathlib.Path("./doc/example/three_maps_input.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    height = 1000
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--limit", hex(height),
                "--threshold", hex(200),
                "--trim_whitespace"
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 186)
        assert file_setup["table_image"].exists()


# @pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/zynqmp_example"}], indirect=True)
# def test_generate_doc_example(file_setup, zynqmp):
#     """ """
    
#     input_file = pathlib.Path("./doc/example/zynqmp.json")
#     with input_file.open("w") as fp:
#         fp.write(json.dumps(zynqmp, indent=2))

#     with unittest.mock.patch(
#         "sys.argv",
#             [
#                 "mm.diagram",
#                 "--file", str(input_file),
#                 "--out", str(file_setup["report"]),
#                 "--threshold", hex(100),
#                 "-l", hex(1000),
#             ],
#         ):

#         mm.diagram.Diagram()

#         assert file_setup["diagram_image"].exists()
#         assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 1000)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/region_exceeds_height-no_maxaddress_set"}], indirect=True)
def test_generate_doc_region_exceeds_height_no_maxaddress_set(file_setup, zynqmp):
    """ 
    -   A4 size diagram, but region exceeds that height. 
        Output should remain at A4 size but the drawing ratio will adjust to fit the larger contents
        Note the ratio is rounded up to nearest integer value.
    -   The 'max_address' is calculated from the region data"""
    
    zynqmp['height'] = 2480
    zynqmp['width'] = 3508

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/region_exceeds_height-no_maxaddress_set.json")
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
                assert mmap.max_address == 4016
                assert mmap.max_address_calculated == True
                assert mmap.draw_scale == 2
            if mname == 'Flash':
                # only one region so this is simply "Boot Image" size
                assert mmap.max_address == int("0xFFFFFF", 16)
                assert mmap.max_address_calculated == True
                assert mmap.draw_scale == 6766

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (3508, 2480)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/region_freespace_exceeds_height-higher_maxaddress_set"}], indirect=True)
def test_generate_doc_region_freespace_exceeds_height_higher_maxaddress_set(file_setup, zynqmp, caplog):
    """ 
    same as 'test_generate_doc_region_exceeds_height_no_maxaddress_set' test, but:
    -   'max_address' is now set at a higher value than the max region size. 
        This will cause excessive freespace values to be created (larger than the diagram height).
        To prevent illegible diagrams, the pre-calculated value will be used instead.
    """
    
    zynqmp['height'] = 2480
    zynqmp['width'] = 3508

    zynqmp['memory_maps']['Flash']['max_address'] = "0xFFFFFFFF"
    zynqmp['memory_maps']['Global System Address Map']['max_address'] = "0xFFFFFFFF"

    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['size'] = "0xFFFFFF"
    # "Boot Image" won't match ["Global System Address Map", "OCM"] link at this size
    zynqmp['memory_maps']['Flash']['memory_regions']['Boot Image']['links'] = []

    input_file = pathlib.Path("./doc/example/region_freespace_exceeds_height-higher_maxaddress_set.json")
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

            # 
            assert "Region freespace exceeds diagram height" in caplog.text

            mmap: mm.metamodel.MemoryMap
            for mname, mmap in d.model.memory_maps.items():
                if mname == 'Global System Address Map':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_calculated == False
                    assert mmap.draw_scale == 2
                if mname == 'Flash':
                    # overridden by user
                    assert mmap.max_address == int("0xFFFFFFFF", 16)
                    assert mmap.max_address_calculated == False
                    # NOTE: draw_scale has been adjusted because it didn't allow space for a void region
                    assert mmap.draw_scale == 6866

            

            assert file_setup["diagram_image"].exists()
            assert PIL.Image.open(str(file_setup["diagram_image"])).size == (3508, 2480)