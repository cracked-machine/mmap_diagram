import unittest
import pytest
import mm.diagram
import pathlib
import PIL.Image

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
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()


def test_arg_tuple():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '0x10']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '0x10',
                              '0x10']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10']):
        mm.diagram.MemoryMap()


def test_invalid_region_data_format1():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '10',
                              '0x10']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()


def test_invalid_region_data_format2():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '10',
                              '0x10']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()


def test_invalid_region_data_formatBoth():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '10',
                              '10']):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()


def test_invalid_out_arg():
    ''' output path should end in .md  '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o",
                              f"/tmp/pytest/{__name__}.txt"]):
        with pytest.raises(NameError):
            mm.diagram.MemoryMap()


def test_invalid_duplicate_name_arg():
    """there can only be one."""
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              'a',
                              '0x10',
                              '0x10']):
        with pytest.warns(RuntimeWarning):
            mm.diagram.MemoryMap()


def test_valid_custom_out_arg(setup):
    ''' should create custom report dir/files '''
    
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report'])
                              ]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


def test_scale_arg_as_hex(setup):
    ''' should create custom report dir/files '''
    
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-s", "3"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


def test_scale_arg_as_int(setup):
    ''' should create custom report dir/files '''
    
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-s", "3"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


def test_invalid_2000_limit_arg_format(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-l", "2000"]):
        with pytest.raises(SystemExit):
            mm.diagram.MemoryMap()
        assert not setup['report'].exists()
        assert not setup['image_full'].exists()
        assert not setup['image_cropped'].exists()


def test_default_limit_arg_format(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report'])
                              ]):

        d = mm.diagram.MemoryMap()
        default_limit = d.args.limit

        # this test assumes the default 'voidthreshold' is 0x3e8 (1000)
        assert d.args.voidthreshold == hex(1000)
        assert not d.args.voidthreshold == 1000

        assert setup['report'].exists()

        assert setup['image_full'].exists()
        outimg = PIL.Image.open(str(setup['image_full']))
        assert hex(outimg.size[1]) == default_limit

        assert setup['image_cropped'].exists()
        outimg = PIL.Image.open(str(setup['image_cropped']))
        assert hex(outimg.size[1]) == default_limit


def test_valid_2000_limit_arg_format(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-l", hex(2000)]):

        d = mm.diagram.MemoryMap()

        # make sure arg was set as hex
        assert d.args.limit == hex(2000)
        assert not d.args.limit == 2000

        assert setup['report'].exists()

        assert setup['image_full'].exists()
        outimg = PIL.Image.open(str(setup['image_full']))
        assert outimg.size[1] == 2000

        assert setup['image_cropped'].exists()
        outimg = PIL.Image.open(str(setup['image_cropped']))
        assert outimg.size[1] == 112


def test_voidthresh_arg(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-v", "0x3e8"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


