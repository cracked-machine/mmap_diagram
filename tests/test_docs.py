import unittest
import mm.diagram
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input
import json

@pytest.fixture
def setup(request):

    report = pathlib.Path(f"doc/example/{__name__}{request.param['file_prefix']}.md")
    report.unlink(missing_ok=True)

    image_full = pathlib.Path(f"doc/example/{__name__}{request.param['file_prefix']}_full.png")
    image_full.unlink(missing_ok=True)

    image_cropped = pathlib.Path(f"doc/example/{__name__}{request.param['file_prefix']}_cropped.png")
    image_cropped.unlink(missing_ok=True)

    return {"report": report, "image_full": image_full, "image_cropped": image_cropped}


@pytest.mark.parametrize("setup", [{"file_prefix": "_normal"}], indirect=True)
def test_generate_doc_example_normal(setup):
    """ """

    diagram_height = 1000
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(setup["report"]),
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

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        found_size = PIL.Image.open(str(setup["image_full"])).size
        assert found_size == (400, diagram_height)

        # reduced void threshold, so empty section between rootfs and dtb should be voided, making the file smaller
        assert setup["image_cropped"].exists()
        found_size = PIL.Image.open(str(setup["image_cropped"])).size
        assert found_size == (400, 338)


@pytest.mark.parametrize("setup", [{"file_prefix": "_collisions"}], indirect=True)
def test_generate_doc_example_collisions(setup):
    """ """
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x50",
            "dtb", "0x90", "0x30",
            "-o", str(setup["report"]),
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

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        assert setup["image_cropped"].exists()

@pytest.mark.parametrize("setup", [{"file_prefix": "_two_maps"}], indirect=True)
def test_generate_doc_example_two_maps(input, setup):
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
                "-o", str(setup["report"]),
                "-l", hex(diagram_height),
                "-v", hex(200),
            ],
        ):

        

        mm.diagram.Diagram()

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        assert setup["image_cropped"].exists()

@pytest.mark.parametrize("setup", [{"file_prefix": "_three_maps"}], indirect=True)
def test_generate_doc_example_three_maps(input, setup):
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
                "-o", str(setup["report"]),
                "-l", hex(diagram_height),
                "-v", hex(200),
            ],
        ):

        mm.diagram.Diagram()

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        assert setup["image_cropped"].exists()