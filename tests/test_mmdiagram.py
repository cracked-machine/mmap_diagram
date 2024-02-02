import mmdiagram.generator
import unittest 
import pytest

def test_arg_pair():
    with unittest.mock.patch('sys.argv', ['mmap_digram.diagram', '0x10']):
        with pytest.raises(SystemExit):
            mmdiagram.generator.Diagram()

    with unittest.mock.patch('sys.argv', ['mmap_digram.diagram', '0x10', '0x10']):
            mmdiagram.generator.Diagram()

def test_no_args():
    with unittest.mock.patch('sys.argv', ['mmap_digram.diagram', '']):
        with pytest.raises(SystemExit):
            mmdiagram.generator.Diagram()
