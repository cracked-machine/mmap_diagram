import mm.diagram
import unittest
import mm.types
import PIL.Image
import pathlib


def test_scaling_x1():
    """  """
    default_diagram_width = 400
    requested_diagram_height = 400
    requested_scale = 1
    report_path = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    image_path = pathlib.Path(f"/tmp/pytest/{__name__}.png")
    report_path.unlink(missing_ok=True)
    image_path.unlink(missing_ok=True)

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x30',
                              'rootfs',
                              '0x50',
                              '0x30',
                              'dtb',
                              '0x90',
                              '0x30',
                              "-o",
                              str(report_path),
                              "-l",
                              str(requested_diagram_height)]):

        d = mm.diagram.MemoryMap()
        outimg = PIL.Image.open(str(image_path))
        assert d.height == requested_diagram_height * requested_scale
        assert d.width == default_diagram_width * requested_scale
        assert outimg.size == (d.width, d.height)


def test_scaling_x2():
    """  """
    default_diagram_width = 400
    requested_diagram_height = 400
    requested_scale = 2
    report_path = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    image_path = pathlib.Path(f"/tmp/pytest/{__name__}.png")
    report_path.unlink(missing_ok=True)
    image_path.unlink(missing_ok=True)

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x30',
                              'rootfs',
                              '0x50',
                              '0x30',
                              'dtb',
                              '0x90',
                              '0x30',
                              "-o", str(report_path),
                              "-l", str(requested_diagram_height),
                              "-s", str(requested_scale)]):

        d = mm.diagram.MemoryMap()
        outimg = PIL.Image.open(str(image_path))
        assert d.height == requested_diagram_height * requested_scale
        assert d.width == default_diagram_width * requested_scale
        assert outimg.size == (d.width, d.height)
