import mm.diagram
import unittest
import mm.image
import pathlib
import PIL.Image
import pytest
from tests.common_fixtures import file_setup

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_void_region_default"}], indirect=True)
def test_void_region_default(file_setup):
    """ """

    diagram_height = 2000
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "-o", str(file_setup["report"]),
            "-l", hex(diagram_height),
        ],
    ):

        d = mm.diagram.Diagram()

        # assumes the defaults haven't changed
        assert mm.diagram.Diagram.pargs.scale == 1
        assert mm.diagram.Diagram.pargs.voidthreshold == hex(1000)

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
        assert found_size == (400, 530)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_void_region_uservalue_500"}], indirect=True)
def test_void_region_uservalue_500(file_setup):
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
            "-v", hex(500),
        ],
    ):

        d = mm.diagram.Diagram()

        # assumes the defaults haven't changed
        assert mm.diagram.Diagram.pargs.scale == 1

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
        assert found_size == (400, 530)

        assert file_setup["table_image"].exists()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_void_region_uservalue_200"}], indirect=True)
def test_void_region_uservalue_200(file_setup):
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
        assert found_size == (400, 352)

        assert file_setup["table_image"].exists()