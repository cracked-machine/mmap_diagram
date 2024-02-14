# import mm.diagram
# import unittest
# import pytest
# import mm.types


# # def test_no_more_colours_but_white():
# #     """ white is a forbidden colour and thare are not enough colours left for 3 regions
# #     so it should pass with error """
# #     with unittest.mock.patch('sys.argv',
# #                              ['mm.diagram',
# #                               'kernel',
# #                               '0x10',
# #                               '0x60',
# #                               'rootfs',
# #                               '0x50',
# #                               '0x10',
# #                               'dtb',
# #                               '0x10',
# #                               '0x150',
# #                               "-o",
# #                               f"/tmp/pytest/{__name__}.md"]):
# #         # deliberately restrict the dict len=1 so we can confirm the error is raised.
# #         with unittest.mock.patch('mm.types.MemoryRegion._remaining_colours',
# #                                  {"white": "#000000"}):
# #             with pytest.raises(SystemExit):
# #                 mm.diagram.MemoryMap()


# def test_no_more_colours_but_black():
#     """ black is not a forbidden colour but thare are not enough colours left for 3 regions
#     so it should pass with error """
#     with unittest.mock.patch('sys.argv',
#                              ['mm.diagram',
#                               'kernel',
#                               '0x10',
#                               '0x60',
#                               'rootfs',
#                               '0x50',
#                               '0x10',
#                               'dtb',
#                               '0x10',
#                               '0x150',
#                               "-o",
#                               f"/tmp/pytest/{__name__}.md"]):
#         # deliberately restrict the dict len=1 so we can confirm the error is raised.
#         with unittest.mock.patch('mm.types.MemoryRegion._remaining_colours',
#                                  {"black": "#ffffff"}):
#             with pytest.raises(SystemExit):
#                 mm.diagram.MemoryMap()


# def test_only_one_lightslategr_y():
#     """ make sure 'lightslategray' is removed from the colour list """
#     with unittest.mock.patch('sys.argv',
#                              ['mm.diagram',
#                               'kernel', '0x10', '0x60',
#                               'rootfs', '0x50', '0x10'
#                               "-o", f"/tmp/pytest/{__name__}.md"],
#                              'mm.types.MemoryRegion._remaining_colours',
#                              {"lightslategray": "#778899", "lightslategrey": "#778899"}):
#         with pytest.raises(SystemExit):
#             mm.diagram.MemoryMap()
