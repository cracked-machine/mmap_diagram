import unittest
import mm.diagram


def test_generate_doc_example():
    """  """
    with unittest.mock.patch('sys.argv',
                             ['mmap_digram.diagram',
                              'kernel',
                              '0x10',
                              '0x50',
                              'rootfs',
                              '0x50',
                              '0x30',
                              'dtb',
                              '0x90',
                              '0x30',
                              'uboot',
                              '0xD0',
                              '0x50',
                              'uboot-scr',
                              '0x110',
                              '0x30',
                              "-o", "doc/example/report.md",
                              "-s", "2"],
                             ):
        d = mm.diagram.MemoryMap()
        for region in d._region_list:
            if region.name == "kernel":
                assert region._origin == "0x10"
                assert region._size == "0x50"
                assert region.remain == "-0x10"
            if region.name == "rootfs":
                assert region._origin == "0x50"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "dtb":
                assert region._origin == "0x90"
                assert region._size == "0x30"
                assert region.remain == "0x10"
            if region.name == "uboot":
                assert region._origin == "0xD0"
                assert region._size == "0x50"
                assert region.remain == "-0x10"
            if region.name == "uboot-scr":
                assert region._origin == "0x110"
                assert region._size == "0x30"
                assert region.remain == "0x50"
