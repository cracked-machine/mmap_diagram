import unittest
import pytest
import mm.diagram
import pathlib


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
                              "-s", "0x3"]):
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


def test_limit_arg_as_hex(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-l", "0x3e8"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


def test_limit_arg_as_int(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-l", "1000"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()


def test_voidthresh_arg_as_hex(setup):
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


def test_voidthresh_arg_as_int(setup):
    ''' should create custom report dir/files '''

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o", str(setup['report']),
                              "-v", "1000"]):
        mm.diagram.MemoryMap()
        assert setup['report'].exists()
        assert setup['image_full'].exists()
        assert setup['image_cropped'].exists()
