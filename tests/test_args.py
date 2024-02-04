import unittest
import pytest
import mm.diagram
import pathlib

# Check the output report at /tmp/pytest/tests.test_args.md


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


def test_valid_default_out_arg():
    ''' should create default report dir/files  '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10']):
        mm.diagram.MemoryMap()
        assert pathlib.Path("out/report.md").exists()
        assert pathlib.Path("out/report.png").exists()


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


def test_valid_custom_out_arg():
    ''' should create custom report dir/files '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o",
                              f"/tmp/pytest/{__name__}.md"]):
        mm.diagram.MemoryMap()
        assert pathlib.Path(f"/tmp/pytest/{__name__}.md").exists()
        assert pathlib.Path(f"/tmp/pytest/{__name__}.png").exists()
