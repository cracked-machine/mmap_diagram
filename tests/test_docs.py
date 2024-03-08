import unittest
import mm.diagram
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input, file_setup, zynqmp, zynqmp_large, zynqmp_max_address_exceeds_regions
import json


@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_normal"}], indirect=True)
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
            "-o", str(file_setup["report"]),
            "-l", hex(height),
            "-t", hex(200),
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

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_collisions"}], indirect=True)
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
            "-o", str(file_setup["report"]),
            "-l", height,
            "-t", hex(200),
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

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_two_maps"}], indirect=True)
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
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-l", hex(height),
                "-t", hex(200),
            ],
        ):

        

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 130)


        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_example_three_maps"}], indirect=True)
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
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-l", hex(height),
                "-t", hex(200),
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 186)
        assert file_setup["table_image"].exists()


@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_zynqmp_example"}], indirect=True)
def test_generate_doc_zynqmp_example(file_setup, zynqmp):
    """ """
    
    input_file = pathlib.Path("./doc/example/zynqmp.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-t", hex(100),
                "-l", hex(1000),
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (1000, 1000)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_zynqmp_large_example"}], indirect=True)
def test_generate_doc_zynqmp_large_example(file_setup, zynqmp_large):
    """ """
    
    input_file = pathlib.Path("./doc/example/zynqmp_large.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp_large, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-t", hex(100)
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (3508, 2480)

@pytest.mark.parametrize("file_setup", [{"file_path": "doc/example/test_generate_doc_zynqmp_max_address_exceeds_regions"}], indirect=True)
def test_generate_doc_zynqmp_max_address_exceeds_regions(file_setup, zynqmp_max_address_exceeds_regions):
    """ """
    
    input_file = pathlib.Path("./doc/example/zynqmp_large.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(zynqmp_max_address_exceeds_regions, indent=2))

    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "-f", str(input_file),
                "-o", str(file_setup["report"]),
                "-t", hex(100)
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (3508, 1119)