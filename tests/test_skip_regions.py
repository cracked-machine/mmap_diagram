import mm.diagram
import unittest
import mm.types
import pathlib
import PIL.Image
import pytest


@pytest.fixture
def setup():
    report = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    report.unlink(missing_ok=True)

    image_full = pathlib.Path(f"/tmp/pytest/{__name__}_full.png")
    image_full.unlink(missing_ok=True)

    image_cropped = pathlib.Path(f"/tmp/pytest/{__name__}_cropped.png")
    image_cropped.unlink(missing_ok=True)

    return {"report": report, "image_full": image_full, "image_cropped": image_cropped}


def test_skip_region(setup):
    """  """

    diagram_height = 1000
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x30',
                              'rootfs',
                              '0x50',
                              '0x30',
                              'dtb',
                              '0x190',
                              '0x30',
                              "-o", str(setup['report']),
                              "-l", str(diagram_height)]):

        d = mm.diagram.MemoryMap()
        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x30"
                assert region.remain == "0x110"
            if region.name == "dtb":
                assert region._origin == "0x190"
                assert region._size == "0x30"
                assert region.remain == "0x228"

        assert setup['report'].exists()

        assert setup['image_full'].exists()
        assert PIL.Image.open(str(setup['image_full'])).width == 400
        assert PIL.Image.open(str(setup['image_full'])).height == 1000

        assert setup['image_cropped'].exists()
        assert PIL.Image.open(str(setup['image_cropped'])).width == 400
        assert PIL.Image.open(str(setup['image_cropped'])).height == 316
