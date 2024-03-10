import mm.diagram
import unittest
import mm.image
import pathlib
import PIL.Image
import pytest
import json
from tests.common_fixtures import file_setup, input

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_default"}], indirect=True)
def test_void_region_default(file_setup):
    """ """

    height = 2000
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(height),
            
        ],
    ):

        d = mm.diagram.Diagram()

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
                assert region_image.freespace_as_hex == "0x610"

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (400, 288)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_uservalue_500"}], indirect=True)
def test_void_region_uservalue_500(file_setup):
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
            "-t", hex(500),
            
        ],
    ):

        d = mm.diagram.Diagram()

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
        assert found_size == (400, 516)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_uservalue_1000"}], indirect=True)
def test_void_region_uservalue_1000(file_setup):
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
            "-t", hex(1000),
            
        ],
    ):

        d = mm.diagram.Diagram()

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
        assert found_size == (400, 482)

        assert file_setup["table_image"].exists()


@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/void_region_uservalue_file"}], indirect=True)
def test_void_region_uservalue_file(file_setup, input):
    """ """

    input_file = pathlib.Path("./out/tmp/void_region_uservalue_file.json")
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
        for mmd in d.mmd_list:
            assert not "kernel" in mmd.image_list
            assert not "rootfs" in mmd.image_list
            assert not "dtb" in mmd.image_list

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        found_size = PIL.Image.open(str(file_setup["diagram_image"])).size
        assert found_size == (1000, 130)

        assert file_setup["table_image"].exists()