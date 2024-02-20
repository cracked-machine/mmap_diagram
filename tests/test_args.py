import unittest
import pytest
import mm.diagram
import pathlib
import PIL.Image
import argparse
import pydantic

@pytest.fixture
def setup():
    report = pathlib.Path(f"/tmp/pytest/{__name__}.md")
    image_full = pathlib.Path(f"/tmp/pytest/{__name__}_full.png")
    image_cropped = pathlib.Path(f"/tmp/pytest/{__name__}_cropped.png")
    report.unlink(missing_ok=True)
    image_full.unlink(missing_ok=True)
    image_cropped.unlink(missing_ok=True)
    return {"report": report, "image_full": image_full, "image_cropped": image_cropped}


def test_no_args():
    with unittest.mock.patch("sys.argv", ["mm.diagram", ""]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()


def test_arg_tuple():
    with unittest.mock.patch("sys.argv", ["mm.diagram", "0x10"]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

    with unittest.mock.patch("sys.argv", ["mm.diagram", "0x10", "0x10"]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10"]):
        mm.diagram.Diagram()


def test_invalid_region_data_format1():
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "0x10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_region_data_format2():
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "0x10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_region_data_formatBoth():
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_out_arg():
    """output path should end in .md"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10", "-o", f"/tmp/pytest/{__name__}.txt"]):
        with pytest.raises(NameError):
            mm.diagram.Diagram()


def test_invalid_duplicate_name_arg():
    """there can only be one."""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10", "a", "0x10", "0x10"]):
        d = mm.diagram.Diagram()
        # the second memregion would have been skipped so we should only have one mem region
        memmap_name = list(d.model.memory_maps.keys())[0]
        assert len(d.model.memory_maps[memmap_name].memory_regions) == 1

def test_scale_arg():
    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-s", "3"]):
        
        mm.diagram.Diagram()

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-s", "0x3"]):
        
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

def test_voidthresh_arg():
    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-v", "1000"]):
        
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-v", "0x3e8"]):
        
        mm.diagram.Diagram()
        
def test_invalid_2000_limit_arg_format(setup):
    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-l", "2000"]):
        
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

def test_default_limit_arg_format(setup):
    """should create custom report dir/files"""

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-o", str(setup["report"])]):

        mm.diagram.Diagram()
        default_limit = mm.diagram.Diagram.pargs.limit

        # this test assumes the default 'voidthreshold' is 0x3e8 (1000)
        assert mm.diagram.Diagram.pargs.voidthreshold == hex(1000)
        assert not mm.diagram.Diagram.pargs.voidthreshold == 1000

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        outimg = PIL.Image.open(str(setup["image_full"]))
        assert hex(outimg.size[1]) == default_limit

        assert setup["image_cropped"].exists()
        outimg = PIL.Image.open(str(setup["image_cropped"]))
        assert hex(outimg.size[1]) == default_limit


def test_valid_2000_limit_arg_format(setup):
    """should create custom report dir/files"""

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-o", str(setup["report"]), 
         "-l", hex(2000)]
    ):

        mm.diagram.Diagram()

        # make sure arg was set as hex
        assert mm.diagram.Diagram.pargs.limit == hex(2000)
        assert not mm.diagram.Diagram.pargs.limit == 2000

        assert setup["report"].exists()

        assert setup["image_full"].exists()
        outimg = PIL.Image.open(str(setup["image_full"]))
        assert outimg.size[1] == 2000

        assert setup["image_cropped"].exists()
        outimg = PIL.Image.open(str(setup["image_cropped"]))
        assert outimg.size[1] == 112
