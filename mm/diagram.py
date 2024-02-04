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

    height = 1000
    """height of the diagram image"""
    width = 500
    """width of the diagram image"""
    bgcolour = "oldlace"

    def __init__(self):
        self._legend_width = 50
        """width of the area used for text annotations/legend"""
        self._region_list = None
        """List of region objects"""

        logging.debug("")
        # create a list of region objects populated with input data
        self._region_list = self._process_input()
        # sort in descending order so largest regions are drawn first in z-order (background)
        self._region_list.sort(key=lambda x: x.size, reverse=True)
        # output image diagram
        self._create_diagram(self._region_list)
        # output markdown report (refs image)
        self._create_markdown(self._region_list)

    def _create_diagram(self, region_list: List[mm.types.Region]):

        # init the main image
        img_main = PIL.Image.new("RGB", (MemoryMap.width, MemoryMap.height), color=MemoryMap.bgcolour)

        # this is the x-axis drawing offset for each region
        # we increment this each time we draw a region to clearly show overlaps
        region_offset = 0

        # add a new layer (region_img) for each region block
        # to the main image object (img_main)
        for region in region_list:

            logging.info(region)
            if not region.size:
                logging.warning("Zero size region skipped")
                continue

            region_offset = region_offset + 5

            ### Region Blocks and text
            region_img = PIL.Image.new("RGBA", (MemoryMap.width - self._legend_width, region.size), color=(255, 255, 0, 5))
            region_canvas = PIL.ImageDraw.Draw(region_img)

            region_canvas.rectangle(
                (0, 0, MemoryMap.width - 1, region.origin + region.size),
                fill=region.colour,
                outline="black",
                width=1,
            )
            
            # draw name text
            ntext_img_width = 60
            ntext_img_height = 7
            ntext_font = PIL.ImageFont.load_default(ntext_img_height)
            ntext_img = PIL.Image.new(
                "RGB",
                (ntext_img_width, ntext_img_height),
                color=MemoryMap.bgcolour)
            
            ntext_canvas = PIL.ImageDraw.Draw(ntext_img)
            
            _, _, ntext_width, ntext_height = ntext_canvas.textbbox(
                (0, 0),
                region.name, 
                font=ntext_font)
            
            ntext_canvas.text(
                ((ntext_img_width-ntext_width)/2,
                 (ntext_img_height-ntext_height)/2-1),
                region.name, fill="black",
                font=ntext_font)
            
            ntext_img = ntext_img.rotate(180)
            region_img.paste(ntext_img, (5, 5))


            ### Address Text
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

            # paste all the layers onto the main image
            img_main.paste(region_img, (self._legend_width + region_offset, region.origin), region_img)
            img_main.paste(endaddr_text_img, (0, endaddr - 6))
            img_main.paste(origin_text_img, (0, region.origin - 4))
            
        # 0,0 should start lower right, not upper left
        img_main = img_main.rotate(180)

        # output image file
        img_file = pathlib.Path(self.args.out).stem + ".png"
        img_main.save(pathlib.Path(self.args.out).parent / img_file)

    def _create_markdown(self, region_list: List[mm.types.Region]):
        with open(self.args.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(self.args.out).stem}.png)\n""")
            f.write("|name|origin|size|remaining|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for region in region_list:
                f.write(f"{region}\n")

    def _process_input(self) -> List[mm.types.Region]:

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("regions", help='command line input for regions should be tuples of name, origin and size.',
                                 nargs="*")
        self.parser.add_argument("-o", "--out", help='path to the markdown output report file. Defaults to "out/report.md"',
                                 default="out/report.md")
        self.args = self.parser.parse_args()

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
                warnings.warn(f"Duplicate region names ({name}) are not permitted. Region will be skipped.", RuntimeWarning)
            else:
                region_list.append(mm.types.Region(name, origin, size))

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
