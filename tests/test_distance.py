import unittest
import pytest 
import json
import pathlib

from tests.fixtures.common import test_setup

import mm.diagram
import mm.image

# These tests only check the distance between adjacent regions
# They don't check the output image sizes so we don't care what value we set to the threshold.


def test_distance_three_regions_same_size_no_collisions():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram", 
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x90", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", height,
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
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x90"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x328"


def test_distance_three_regions_touching_no_collisions():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x40", "0x30",
            "dtb", "0x70", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", height,
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x0"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x40"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x0"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x70"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x348"


def test_distance_three_regions_diff_size_no_collisions():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x10",
            "rootfs", "0x50", "0x20",
            "dtb", "0x90", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", height,
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x10"
                assert region_image.freespace_as_hex == "0x30"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x20"
                assert region_image.freespace_as_hex == "0x20"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x90"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x328"


def test_distance_three_regions_bottom_collision():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x30",
            "dtb", "0x90", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", height,
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x60"
                assert region_image.freespace_as_hex == "-0x20"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x90"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x328"


def test_distance_three_regions_bottom_middle_collision():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x60",
            "rootfs", "0x50", "0x50",
            "dtb", "0x90", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", height,
        ],
    ):

        d = mm.diagram.Diagram()

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


def test_distance_five_regions_bottom_top_collision():
    """ """
    height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x50",
            "rootfs", "0x50", "0x30",
            "dtb", "0x90", "0x30",
            "uboot", "0xD0", "0x50",
            "uboot-scr", "0x110", "0x30",
            "-o", f"/tmp/pytest/{__name__}.md",
            "-l", str(height),
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == "0x50"
                assert region_image.freespace_as_hex == "-0x10"
            if region_image.name == "rootfs":
                assert region_image.origin_as_hex == "0x50"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "dtb":
                assert region_image.origin_as_hex == "0x90"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x10"
            if region_image.name == "uboot":
                assert region_image.origin_as_hex == "0xd0"
                assert region_image.size_as_hex == "0x50"
                assert region_image.freespace_as_hex == "-0x10"
            if region_image.name == "uboot-scr":
                assert region_image.origin_as_hex == "0x110"
                assert region_image.size_as_hex == "0x30"
                assert region_image.freespace_as_hex == "0x2a8"

@pytest.mark.parametrize("test_setup", [{"file_path": "out/tmp/distance_collision_with_limit"}], indirect=True)
def test_distance_collision_with_limit(test_setup):
    """ """
    data = {
        "$schema": "../../mm/schema.json",
        "name": "TestDiagram",
        "height": mm.diagram.A10.width,
        "width": mm.diagram.A10.height,
        "memory_maps": {
            "test": {
                "max_address": hex(mm.diagram.A10.height),
                "memory_regions": 
                {
                    "kernel": {
                        "origin": "0x10",
                        "size": hex(mm.diagram.A10.height + 64),
                    }
                }
            }
        }        
    }

    input_file = pathlib.Path("out/tmp/distance_collision_with_limit.json")
    with input_file.open("w") as fp:
        fp.write(json.dumps(data, indent=2))

    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram", 
            "--file", str(input_file),
            "-o", f"out/tmp/distance_collision_with_limit.md",
            "-v"
        ],
    ):

        d = mm.diagram.Diagram()

        # we only have a single mmd in mmd_list for this test
        for region_image in d.mmd_list[0].image_list:
            if region_image.name == "kernel":
                assert region_image.origin_as_hex == "0x10"
                assert region_image.size_as_hex == hex(mm.diagram.A10.height + 64)
                assert region_image.freespace_as_hex == "-0x50"


        assert test_setup["report"].exists()

        assert test_setup["diagram_image"].exists()
        # outimg = PIL.Image.open(str(test_setup["diagram_image"]))
        # assert outimg.size[1] == 2000

        assert test_setup["table_image"].exists()