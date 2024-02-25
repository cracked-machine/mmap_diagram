import mm.diagram
import unittest
import mm.image
import PIL.Image
import pathlib
import pytest


@pytest.fixture
def setup():
    report = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    image_full = pathlib.Path(f"/tmp/pytest/{__name__}_full.png")
    image_cropped = pathlib.Path(f"/tmp/pytest/{__name__}_cropped.png")
    report.unlink(missing_ok=True)
    image_full.unlink(missing_ok=True)
    image_cropped.unlink(missing_ok=True)
    return {"report": report, "image_full": image_full, "image_cropped": image_cropped}


def assert_expected_scale(
    d: mm.diagram.Diagram, img_path: pathlib.Path, width: int, height: int, cropped_height: int, scale: int
):
    from mm.diagram import Diagram
    assert img_path.exists()
    outimg = PIL.Image.open(str(img_path))
    assert Diagram.model.diagram_height == height * scale
    assert Diagram.model.diagram_width == width * scale
    assert outimg.size == (Diagram.model.diagram_width, cropped_height)


def test_scaling_x1(setup):
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
            str(setup["report"]),
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
            img_path=setup["image_full"],
            width=default_diagram_width,
            height=requested_diagram_height,
            cropped_height=requested_diagram_height,
            scale=requested_scale,
        )

        # cropped height should disregard scaling on cropped image
        assert_expected_scale(
            d,
            img_path=setup["image_cropped"],
            width=default_diagram_width,
            height=requested_diagram_height,
            cropped_height=expected_cropped_height,
            scale=requested_scale,
        )


def test_scaling_x2(setup):
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
            str(setup["report"]),
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

        assert setup["image_full"].exists()
        outimg = PIL.Image.open(str(setup["image_full"]))
        assert Diagram.model.diagram_height == requested_diagram_height * requested_scale
        assert Diagram.model.diagram_width == default_diagram_width * requested_scale
        assert outimg.size == (Diagram.model.diagram_width, Diagram.model.diagram_height)

        assert setup["image_cropped"].exists()
        outimg = PIL.Image.open(str(setup["image_cropped"]))
        assert Diagram.model.diagram_height == requested_diagram_height * requested_scale
        assert Diagram.model.diagram_width == default_diagram_width * requested_scale
        assert outimg.size == (Diagram.model.diagram_width, expected_cropped_height)

        # # cropped height should just be x2 scale on full image, i.e. not cropped at all
        # assert_expected_scale(d,
        #                       img_path=setup['image_full'],
        #                       width=default_diagram_width,
        #                       height=requested_diagram_height,
        #                       cropped_height=requested_diagram_height * requested_scale,
        #                       scale=requested_scale)

        # # cropped height should disregard scaling on cropped image
        # assert_expected_scale(d,
        #                       img_path=setup['image_cropped'],
        #                       width=default_diagram_width,
        #                       height=requested_diagram_height,
        #                       cropped_height=expected_cropped_height,
        #                       scale=requested_scale)
