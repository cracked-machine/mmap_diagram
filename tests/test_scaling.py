import mm.diagram
import unittest
import mm.image
import PIL.Image
import pathlib
import pytest
from tests.common_fixtures import input, file_setup


def assert_expected_scale(
    d: mm.diagram.Diagram, img_path: pathlib.Path, width: int, height: int, cropped_height: int, scale: int
):
    from mm.diagram import Diagram
    assert img_path.exists()
    outimg = PIL.Image.open(str(img_path))
    assert Diagram.model.diagram_height == height * scale
    assert Diagram.model.diagram_width == width * scale
    assert outimg.size == (Diagram.model.diagram_width, cropped_height)

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_scaling_x1"}], indirect=True)
def test_scaling_x1(file_setup):
    """ """
    default_diagram_width = 400
    requested_diagram_height = 2000
    expected_cropped_height = 284
    requested_scale = 1

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
            str(file_setup["report"]),
            "-l",
            hex(requested_diagram_height),
        ],
    ):

        d = mm.diagram.Diagram()

        # assumes default 'voidthreshold' is still 0x3e8 (1000)
        assert mm.diagram.Diagram.pargs.voidthreshold == hex(1000)
        # assume default 'scale' is still x1
        assert mm.diagram.Diagram.pargs.scale == 1

        # cropped height should just be x1 scale on full image, i.e. not cropped at all
        assert_expected_scale(
            d,
            img_path=file_setup["image_full"],
            width=default_diagram_width,
            height=requested_diagram_height,
            cropped_height=requested_diagram_height,
            scale=requested_scale,
        )

        # cropped height should disregard scaling on cropped image
        assert_expected_scale(
            d,
            img_path=file_setup["image_cropped"],
            width=default_diagram_width,
            height=requested_diagram_height,
            cropped_height=expected_cropped_height,
            scale=requested_scale,
        )

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_scaling_x2"}], indirect=True)
def test_scaling_x2(file_setup):
    """ """
    default_diagram_width = 400
    requested_diagram_height = 1000
    expected_cropped_height = 284
    requested_scale = 2

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
            str(file_setup["report"]),
            "-l",
            hex(requested_diagram_height),
            "-s",
            str(requested_scale),
        ],
    ):
        from mm.diagram import Diagram
        Diagram()

        # assumes default haven't changed
        assert Diagram.pargs.voidthreshold == hex(1000)

        assert file_setup["image_full"].exists()
        outimg = PIL.Image.open(str(file_setup["image_full"]))
        assert Diagram.model.diagram_height == requested_diagram_height * requested_scale
        assert Diagram.model.diagram_width == default_diagram_width * requested_scale
        assert outimg.size == (Diagram.model.diagram_width, Diagram.model.diagram_height)

        assert file_setup["image_cropped"].exists()
        outimg = PIL.Image.open(str(file_setup["image_cropped"]))
        assert Diagram.model.diagram_height == requested_diagram_height * requested_scale
        assert Diagram.model.diagram_width == default_diagram_width * requested_scale
        assert outimg.size == (Diagram.model.diagram_width, expected_cropped_height)

        # # cropped height should just be x2 scale on full image, i.e. not cropped at all
        # assert_expected_scale(d,
        #                       img_path=file_setup['image_full'],
        #                       width=default_diagram_width,
        #                       height=requested_diagram_height,
        #                       cropped_height=requested_diagram_height * requested_scale,
        #                       scale=requested_scale)

        # # cropped height should disregard scaling on cropped image
        # assert_expected_scale(d,
        #                       img_path=file_setup['image_cropped'],
        #                       width=default_diagram_width,
        #                       height=requested_diagram_height,
        #                       cropped_height=expected_cropped_height,
        #                       scale=requested_scale)
