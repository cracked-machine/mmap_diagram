import unittest
import mm.diagram
import mm.metamodel
import pathlib
import pytest
import PIL.Image
from tests.common_fixtures import input, file_setup, markdown_setup
import json

@pytest.mark.parametrize(
        "file_setup", 
        [
            {
                "file_path": "docs/example/example_end_collisions",
                "markdown_comment": "Region collision with diagram max address"
            }
        ], indirect=True)
def test_generate_doc_example_end_collisions(file_setup):
    """ """

    
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "--out", str(file_setup["report"]),
            "-l", hex(mm.diagram.A9.width),
            "--threshold", hex(200),
        ],
    ):

        d = mm.diagram.Diagram()

        output_file = pathlib.Path("docs/example/example_end_collisions.json")
        with output_file.open("w") as fp:
            fp.write(d.model.model_dump_json(indent=2))    

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
                assert region_image.freespace_as_hex == "-0xb"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (mm.diagram.A8.width, mm.diagram.A9.width)

        # reduced void threshold, so empty section between rootfs and dtb should be voided, making the file smaller
        assert file_setup["table_image"].exists()

@pytest.mark.parametrize(
        "file_setup", 
        [
            {
                "file_path": "docs/example/example_region_collisions",
                "markdown_comment": "Region collisions with other regions"
            }
        ], indirect=True)
def test_generate_doc_example_region_collisions(file_setup):
    """ """


    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x50",
            "dtb", "0x90", "0x30",
            "--out", str(file_setup["report"]),
            "--limit", hex(mm.diagram.A9.width),
            "--threshold", hex(200),
        ],
    ):

        d =mm.diagram.Diagram()

        output_file = pathlib.Path("docs/example/example_region_collisions.json")
        with output_file.open("w") as fp:
            fp.write(d.model.model_dump_json(indent=2))    

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
                assert region_image.freespace_as_hex == "0xf5"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A8.width, mm.diagram.A9.width)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize(
        "file_setup", 
        [
            {
                "file_path": "docs/example/example_two_maps",
                "markdown_comment": "Diagram with two memory maps"
            }
        ], indirect=True)
def test_generate_doc_example_two_maps(input, file_setup):
    """ """

    input['height'] = mm.diagram.A9.width
    input['width'] = mm.diagram.A9.height
    input['memory_maps']['eMMC']['memory_regions']['Blob4'] = {
        "origin": "0x100",
        "size": "0x30"
    }

    input['memory_maps']['DRAM']['memory_regions']['Blob5'] = {
        "origin": "0x30",
        "size": "0x10"
    }

    input_file = pathlib.Path("./docs/example/example_two_maps.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    
    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--limit", hex(mm.diagram.A8.height),
                "--threshold", hex(200),
            ],
        ):

        

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A9.height, mm.diagram.A9.width)


        assert file_setup["table_image"].exists()

@pytest.mark.parametrize(
        "file_setup", 
        [
            {
                "file_path": "docs/example/example_three_maps",
                "markdown_comment": "Diagram with three memory maps"
            }
        ], indirect=True)
def test_generate_doc_example_three_maps(input, file_setup):
    
    """ """

    input['height'] = mm.diagram.A9.width
    input['width'] = mm.diagram.A9.height    
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

    input_file = pathlib.Path("./docs/example/example_three_maps.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))


    with unittest.mock.patch(
        "sys.argv",
            [
                "mm.diagram",
                "--file", str(input_file),
                "--out", str(file_setup["report"]),
                "--limit", hex(mm.diagram.A8.height),
                "--threshold", hex(200),
            ],
        ):

        mm.diagram.Diagram()

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        assert PIL.Image.open(str(file_setup["diagram_image"])).size == (mm.diagram.A9.height, mm.diagram.A9.width)
        assert file_setup["table_image"].exists()

######################################
        