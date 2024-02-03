import mmdiagram.generator
import unittest
import pytest
import pathlib

# Test 'data' arguments


def test_no_args():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '']):
        with pytest.raises(SystemExit):
            mmdiagram.generator.Diagram()


def test_arg_tuple():
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '0x10']):
        with pytest.raises(SystemExit):
            mmdiagram.generator.Diagram()

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              '0x10',
                              '0x10']):
        with pytest.raises(SystemExit):
            mmdiagram.generator.Diagram()

    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10']):
        mmdiagram.generator.Diagram()

# Test 'out' argument


def test_invalid_out_arg():
    ''' output path should end in .md  '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o",
                              "/tmp/custom/myreport.txt"]):
        with pytest.raises(NameError):
            mmdiagram.generator.Diagram()


def test_valid_default_out_arg():
    ''' should create default report dir/files  '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10']):
        mmdiagram.generator.Diagram()
        assert pathlib.Path("out/report.md").exists()
        assert pathlib.Path("out/report.png").exists()


def test_valid_custom_out_arg():
    ''' should create custom report dir/files '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'a',
                              '0x10',
                              '0x10',
                              "-o",
                              "/tmp/custom/myreport.md"]):
        mmdiagram.generator.Diagram()
        assert pathlib.Path("/tmp/custom/myreport.md").exists()
        assert pathlib.Path("/tmp/custom/myreport.png").exists()


def test_generate_doc_example():
    ''' should create custom report dir/files '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x60',
                              'rootfs',
                              '0x50',
                              '0x10',
                              'dtb',
                              '0x10',
                              '0x150',
                              "-o",
                              "doc/example/report.md"]):
        mmdiagram.generator.Diagram()
        assert pathlib.Path("doc/example/report.md").exists()
        assert pathlib.Path("doc/example/report.png").exists()