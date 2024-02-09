import mm.diagram
import unittest
import mm.types
import pathlib
import PIL.Image

# Check the output report at /tmp/pytest/tests.test_distance.md


def test_skip_region():
    """  """

    report = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    image_full = pathlib.Path(f"/tmp/pytest/{__name__}_full.png")
    image_crop_join = pathlib.Path(f"/tmp/pytest/{__name__}_cropped.png")

    report.unlink(missing_ok=True)
    image_full.unlink(missing_ok=True)
    image_crop_join.unlink(missing_ok=True)

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
                              "-o", str(report),
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

        assert report.is_file

        assert image_full.is_file
        assert PIL.Image.open(image_full).width == 400
        assert PIL.Image.open(image_full).height == 1000
                
        assert image_crop_join.is_file
        assert PIL.Image.open(image_crop_join).width == 400
        assert PIL.Image.open(image_crop_join).height == 316
