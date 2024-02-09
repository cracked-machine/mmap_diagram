import argparse
import itertools
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
from typing import List
import typeguard

import sys
import pathlib
import mm.types
import warnings

import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


@typeguard.typechecked
class MemoryMap:

    height: int = 400
    """height of the diagram image"""
    width: int = 400
    """width of the diagram image"""
    bgcolour = "oldlace"

    def __init__(self):
        self._legend_width = 100
        """width of the area used for text annotations/legend"""
        self._region_list = None
        """List of region objects"""

        # create a list of region objects populated with input data
        self._region_list = self._process_input()

        # temporarily sort by ascending origin attribute and assign the draw indent
        self._region_list.sort(key=lambda x: x.origin, reverse=False)
        region_indent = 0
        for r in self._region_list:
            r.draw_indent = region_indent
            region_indent += 5

        # sort in descending order so largest regions are drawn first in z-order (background)
        self._region_list.sort(key=lambda x: x.size, reverse=True)

        # output image diagram
        self._create_diagram(self._region_list)
        # output markdown report (refs image)
        self._create_markdown(self._region_list)

    def _create_diagram(self, region_list: List[mm.types.MemoryRegion]):

        # init the main image
        img_main = PIL.Image.new("RGB", (MemoryMap.width, MemoryMap.height), color=MemoryMap.bgcolour)

        # add a new layer (region_img) for each region block
        # to the main image object (img_main)
        for region in region_list:

            region.create_img(img_width=MemoryMap.width - self._legend_width)
            if not region.img:
                continue

            # Address Text
            addr_text_font = PIL.ImageFont.load_default(8)
            # add text for the region origin
            origin_text_img = PIL.Image.new("RGB", (30, 10), color=(255, 255, 255))
            origin_text_canvas = PIL.ImageDraw.Draw(origin_text_img)
            origin_text_canvas.text((0, 0), region._origin, fill="black", font=addr_text_font)
            origin_text_img = origin_text_img.rotate(180)
            # add text for the region end
            endaddr = region.origin + region.size
            endaddr_text_img = PIL.Image.new("RGB", (30, 10), color=(255, 255, 255))
            endaddr_text_canvas = PIL.ImageDraw.Draw(endaddr_text_img)
            endaddr_text_canvas.text((0, 0), hex(endaddr), fill="black", font=addr_text_font)
            endaddr_text_img = endaddr_text_img.rotate(180)

            line_width = 1
            line_canvas = PIL.ImageDraw.Draw(img_main)
            for x in range(40, 90, 4):
                line_canvas.line((x, endaddr - line_width, x+2, endaddr - line_width), fill="black", width=line_width)
                line_canvas.line((x, region.origin - line_width, x+2, region.origin - line_width), fill="black", width=1)
            
            # paste all the layers onto the main image
            img_main.paste(region.img, (self._legend_width + region.draw_indent, region.origin), region.img)
            img_main.paste(endaddr_text_img, (0, endaddr - 6))
            img_main.paste(origin_text_img, (0, region.origin - 4))

        # rotate so the origin is at the bottom
        img_main = img_main.rotate(180)

        # output image file
        img_file = pathlib.Path(self.args.out).stem + ".png"
        img_main.save(pathlib.Path(self.args.out).parent / img_file)

    def _create_markdown(self, region_list: List[mm.types.MemoryRegion]):
        with open(self.args.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(self.args.out).stem}.png)\n""")
            f.write("|name|origin|size|remaining|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for region in region_list:
                f.write(f"{region}\n")

    def _process_input(self) -> List[mm.types.MemoryRegion]:

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("regions", help='command line input for regions should be tuples of name, origin and size.',
                                 nargs="*")
        self.parser.add_argument("-o", "--out", help='path to the markdown output report file. Default: "out/report.md"',
                                 default="out/report.md")
        self.parser.add_argument("-l", "--limit", help="The maximum memory address for the diagram. Default: 400", default=400, type=int)
        self.args = self.parser.parse_args()

        if self.args.limit:
            MemoryMap.height = self.args.limit

        if len(sys.argv) == 1:
            self.parser.error("must pass in data points")
        if len(self.args.regions) % 3:
            self.parser.error("command line input data should be in multiples of three")

        # make sure the output path is valid and parent dir exists
        if not pathlib.Path(self.args.out).suffix == ".md":
            raise NameError("Output file should end with .md")
        pathlib.Path(self.args.out).parent.mkdir(parents=True, exist_ok=True)

        region_list = []
        for r in self._batched(self.args.regions, 3):
            name = r[0]
            origin = r[1]
            size = r[2]
            if any(x.name == name for x in region_list):
                warnings.warn(f"Duplicate region names ({name}) are not permitted. MemoryRegion will be skipped.", RuntimeWarning)
            else:
                region_list.append(mm.types.MemoryRegion(name, origin, size))

        for r in region_list:
            r.calc_nearest_region(region_list)

        return region_list

    def _batched(self, iterable, n):
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch


if __name__ == "__main__":
    MemoryMap()
