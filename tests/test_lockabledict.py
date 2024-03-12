
import unittest
import logging

import mm.diagram

def test_void_no_new_keys(caplog):
    """ Same as 'test_void_region_cli_A5_no_voids' but with json file input"""

    with unittest.mock.patch(
        "sys.argv",
        [
            "mm.diagram",
            "kernel", "0x10", "0x30",
            "rootfs", "0x50", "0x30",
            "dtb", "0x190", "0x30",
            "--limit", hex(1000),
            "--threshold", hex(1000),
            
        ],
    ):

        d = mm.diagram.Diagram()

        assert len(d.mmd_list[0].mixed_region_dict) == 1

        assert all(isinstance(x, mm.image.MemoryRegionImage) for x in d.mmd_list[0].mixed_region_dict[0])
        
        with caplog.at_level(logging.WARNING):
            # make sure you can't add more keys once diagram.py has called lock()
            all(isinstance(x, mm.image.VoidRegionImage) for x in d.mmd_list[0].mixed_region_dict[1])
            assert "You were prevented from trying to update a locked dict!" in caplog.text

        assert len(d.mmd_list[0].mixed_region_dict) == 1