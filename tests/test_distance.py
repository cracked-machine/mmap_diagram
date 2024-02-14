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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x328"


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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x30"
                assert region.remain == "0x0"
            if region.name == "rootfs":
                assert region._origin == "0x40"
                assert region._size == "0x30"
                assert region.remain == "0x0"
            if region.name == "dtb":
                assert region._origin == "0x70"
                assert region._size == "0x30"
                assert region.remain == "0x348"


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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x10"
                assert region.remain == "0x30"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x20"
                assert region.remain == "0x20"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x328"


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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x60"
                assert region.remain == "-0x20"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x328"


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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x60"
                assert region.remain == "-0x20"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x50"
                assert region.remain == "-0x10"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x328"


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

        d = mm.diagram.MemoryMap()

        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x50"
                assert region.remain == "-0x10"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "uboot":
                assert region._origin == "0xD0"
                assert region._size == "0x50"
                assert region.remain == "-0x10"
            if region.name == "uboot-scr":
                assert region._origin == "0x110"
                assert region._size == "0x30"
                assert region.remain == "0x2a8"
