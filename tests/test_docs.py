import unittest
import pathlib
import mmdiagram.generator


def test_generate_doc_example():
    ''' should create custom report dir/files '''
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x60',
                              'rootfs',
                              '0x70',
                              '0x10',
                              'dtb',
                              '0x90',
                              '0x100',
                              "-o",
                              "doc/example/report.md"]):
        mmdiagram.generator.Diagram()
        assert pathlib.Path("doc/example/report.md").exists()
        assert pathlib.Path("doc/example/report.png").exists()
