import mm.diagram
import unittest
import mm.types

# These tests only check the distance between adjacent regions
# They don't check the output image sizes so we don't care what value we set to the voidthreshold.


def test_distance_three_regions_same_size_no_collisions():
    """ """
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x30",
            "rootfs",
            "0x50",
            "0x30",
            "dtb",
            "0x90",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            diagram_height,
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x30",
            "rootfs",
            "0x40",
            "0x30",
            "dtb",
            "0x70",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            diagram_height,
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x10",
            "rootfs",
            "0x50",
            "0x20",
            "dtb",
            "0x90",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            diagram_height,
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x60",
            "rootfs",
            "0x50",
            "0x30",
            "dtb",
            "0x90",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            diagram_height,
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x60",
            "rootfs",
            "0x50",
            "0x50",
            "dtb",
            "0x90",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            diagram_height,
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
    diagram_height = hex(1000)
    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel",
            "0x10",
            "0x50",
            "rootfs",
            "0x50",
            "0x30",
            "dtb",
            "0x90",
            "0x30",
            "uboot",
            "0xD0",
            "0x50",
            "uboot-scr",
            "0x110",
            "0x30",
            "-o",
            f"/tmp/pytest/{__name__}.md",
            "-l",
            str(diagram_height),
        ],
    ):

        d = mm.diagram.Diagram()

        for region_image in d.mm.image_list:
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
