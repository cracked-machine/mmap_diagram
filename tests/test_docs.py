import unittest
import mm.diagram
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input, file_setup
import json


@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_normal"}], indirect=True)
def test_generate_doc_example_normal(file_setup):
    """ """

    diagram_height = 1000
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(diagram_height),
            "-v", hex(200),
        ],
    ):

        d = mm.diagram.Diagram()

        # assumes the defaults haven't changed
        assert mm.diagram.Diagram.pargs.scale == 1

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

        assert file_setup["image_full"].exists()
        found_size = PIL.Image.open(str(file_setup["image_full"])).size
        assert found_size == (400, diagram_height)

        # reduced void threshold, so empty section between rootfs and dtb should be voided, making the file smaller
        assert file_setup["image_cropped"].exists()
        found_size = PIL.Image.open(str(file_setup["image_cropped"])).size
        assert found_size == (400, 328)


@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_collisions"}], indirect=True)
def test_generate_doc_example_collisions(file_setup):
    """ """
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x50",
            "dtb", "0x90", "0x30",
            "-o", str(file_setup["report"]),
            "-l", diagram_height,
            "-v", hex(200),
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

        assert file_setup["image_full"].exists()
        assert file_setup["image_cropped"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_two_maps"}], indirect=True)
def test_generate_doc_example_two_maps(input, file_setup):
    """ """

    input['memory_maps']['eMMC']['memory_regions']['Blob4'] = {
        "memory_region_origin": "0x100",
        "memory_region_size": "0x10"
    }

    input['memory_maps']['DRAM']['memory_regions']['Blob5'] = {
        "memory_region_origin": "0x30",
        "memory_region_size": "0x10"
    }

    input_file = pathlib.Path("./doc/example/two_maps_input.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    diagram_height = 1000
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-l", hex(diagram_height),
                "-v", hex(200),
            ],
        ):

        

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["image_full"].exists()
        assert file_setup["image_cropped"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_three_maps"}], indirect=True)
def test_generate_doc_example_three_maps(input, file_setup):
    """ """
    input["memory_maps"]['flash'] = {
        "map_height": 1000,
        "map_width": 400,                
        "memory_regions": 
        {
            "Blob4": {
            "memory_region_origin": hex(10),
            "memory_region_size": hex(60)
            },
            "Blob5": {
            "memory_region_origin": hex(50),
            "memory_region_size": hex(100)
            },
            "Blob6": {
            "memory_region_origin": hex(80),
            "memory_region_size": hex(150)
            }
        }        
    }

    input_file = pathlib.Path("./doc/example/three_maps_input.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    diagram_height = 1000
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-l", hex(diagram_height),
                "-v", hex(200),
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["image_full"].exists()
        assert file_setup["image_cropped"].exists()