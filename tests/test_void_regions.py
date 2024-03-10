import mm.diagram
import unittest
import mm.image
import pathlib
import PIL.Image
import pytest
import json
from tests.common_fixtures import file_setup, input
from typing import List
import logging

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_cli_defaults"}], indirect=True)
def test_void_region_cli_defaults(file_setup):
    """ Check the void regions were added for the default threshold"""

    
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(mm.diagram.A8.height),
            
        ],
    ):

        d = mm.diagram.Diagram()

        assert len(d.mmd_list[0].mixed_region_dict) == 4
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[0])
        assert all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[1])
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[2])
        assert all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[3])

        # assumes the defaults haven't changed
        assert mm.diagram.Diagram.pargs.threshold == hex(200)

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
                assert region_image.freespace_as_hex == "0x1aa"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (mm.diagram.A8.width, mm.diagram.A8.height)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_cli_a10"}], indirect=True)
def test_void_region_cli_a10(file_setup):
    """ check the voidregions were added for smaller diagram size with lower threshold set"""

    
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x120", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(mm.diagram.A10.height),
            "-t", hex(50),
            
        ],
    ):

        d = mm.diagram.Diagram()

        assert len(d.mmd_list[0].mixed_region_dict) == 4
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[0])
        assert all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[1])
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[2])
        assert all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[3])
        
        for region_image in d.mmd_list[0].image_list:
            
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0xa0"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x120"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x65"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (mm.diagram.A8.width, mm.diagram.A10.height)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_cli_A5_no_voids"}], indirect=True)
def test_void_region_cli_A5_no_voids(file_setup):
    """ check the void regions were not added when the threshold is set above the diagram height"""

    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(mm.diagram.A5.height),
            "-t", hex(5000),
            
        ],
    ):

        d = mm.diagram.Diagram()

        assert len(d.mmd_list[0].mixed_region_dict) == 1
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[0])

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
                assert region_image.freespace_as_hex == "0x7f0"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (mm.diagram.A8.width, mm.diagram.A5.height)

        assert file_setup["table_image"].exists()


@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_uservalue_file_no_voids"}], indirect=True)
def test_void_region_uservalue_file_no_voids(file_setup, input, caplog):
    """ Same as 'test_void_region_cli_A5_no_voids' but with json file input"""

    input_file = pathlib.Path("./out/tmp/void_region_uservalue_file_no_voids.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(input, indent=2))

    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "--out", str(file_setup["report"]),
            "--file", str(input_file),
            "--threshold", hex(1000),
            
        ],
    ):

        d = mm.diagram.Diagram()

        assert len(d.mmd_list[0].mixed_region_dict) == 2
        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[0])
        assert all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[1])

        for mmd in d.mmd_list:
            assert not "kernel" in mmd.image_list
            assert not "rootfs" in mmd.image_list
            assert not "dtb" in mmd.image_list

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (mm.diagram.A8.width, mm.diagram.A8.height)

        assert file_setup["table_image"].exists()