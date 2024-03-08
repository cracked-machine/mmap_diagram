import unittest
import pytest
import mm.diagram
import pathlib
import PIL.Image
import argparse
import pydantic
from tests.common_fixtures import input, file_setup

def test_no_args():
    """This test has no output"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", ""]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()


def test_arg_tuple():
    """Note: output for these test will default to  ./out"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "0x10"]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

    with unittest.mock.patch("sys.argv", ["mm.diagram", "0x10", "0x10"]):
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10"]):
        mm.diagram.Diagram()

    name = "My Memeory Map"
    with unittest.mock.patch("sys.argv", ["mm.diagram", "b", "0x10", "0x10", "-n", name]):
        mm.diagram.Diagram()
        assert name in mm.diagram.Diagram.model.memory_maps


def test_invalid_region_data_format1():
    """Note: output for these test will default to  ./out"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "0x10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_region_data_format2():
    """Note: output for these test will default to  ./out"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "0x10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_region_data_formatBoth():
    """Note: output for these test will default to  ./out"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "10", "10"]):
        with pytest.raises(pydantic.ValidationError):
            mm.diagram.Diagram()


def test_invalid_out_arg():
    """output path should end in .md"""
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10", "-o", f"/tmp/pytest/{__name__}.txt"]):
        with pytest.raises(NameError):
            mm.diagram.Diagram()


def test_invalid_duplicate_name_arg():
    
    with unittest.mock.patch("sys.argv", ["mm.diagram", "a", "0x10", "0x10", "a", "0x10", "0x10"]):
        d = mm.diagram.Diagram()
        # the second memregion would have been skipped so we should only have one mem region
        memmap_name = list(d.model.memory_maps.keys())[0]
        assert len(d.model.memory_maps[memmap_name].memory_regions) == 1

def test_scale_arg():
    """Note: output for these test will default to  ./out"""
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

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_invalid_2000_limit_arg_format"}], indirect=True)
def test_invalid_2000_limit_arg_format(file_setup):
    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-l", "2000"]):
        
        with pytest.raises(SystemExit):
            mm.diagram.Diagram()

@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_default_limit_arg_format"}], indirect=True)
def test_default_limit_arg_format(file_setup):
    """should create custom report dir/files"""

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-o", str(file_setup["report"])]):

        mm.diagram.Diagram()
        default_limit = mm.diagram.Diagram.pargs.limit

        # this test assumes the default 'voidthreshold' is 0x3e8 (1000)
        assert mm.diagram.Diagram.pargs.voidthreshold == hex(1000)
        assert not mm.diagram.Diagram.pargs.voidthreshold == 1000

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        outimg = PIL.Image.open(str(file_setup["diagram_image"]))
        assert outimg.height == 67

        assert file_setup["table_image"].exists()
        
@pytest.mark.parametrize("file_setup", [{"file_path": "out/tmp/test_valid_2000_limit_arg_format"}], indirect=True)
def test_valid_2000_limit_arg_format(file_setup):
    """should create custom report dir/files"""

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "a", "0x10", "0x10", 
         "-o", str(file_setup["report"]), 
         "-l", hex(2000)]
    ):

        mm.diagram.Diagram()

        # make sure arg was set as hex
        assert mm.diagram.Diagram.pargs.limit == hex(2000)
        assert not mm.diagram.Diagram.pargs.limit == 2000

        assert file_setup["report"].exists()

        assert file_setup["diagram_image"].exists()
        outimg = PIL.Image.open(str(file_setup["diagram_image"]))
        assert outimg.size[1] == 116

        assert file_setup["table_image"].exists()

def test_input_file():

    with unittest.mock.patch(
        "sys.argv", 
        ["mm.diagram", 
         "-f", "doc/example/input.json",
         "-l", hex(1000),
         "-v", hex(500)
        ]):
        
        d = mm.diagram.Diagram()
        pass