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
import mmdiagram.types


@typeguard.typechecked
class Diagram:
    def __init__(self):
        self.h = 500
        self.w = 250
        self.legend_width = 50

        self._create_diagram(self._process_input())

    def _create_diagram(self, region_list: List[mmdiagram.types.Region]):

        # init the main image
        img_main = PIL.Image.new("RGB", (self.w, self.h), color=(255, 255, 255))

        # this is the x-axis drawing offset for each region
        # we increment this each time we draw a region to clearly show overlaps
        region_offset = 0

        # add a new layer (region_img) for each region block
        # to the main image object (img_main)
        for region in region_list:

            print(region)
            if not region.size:
                print("Zero size region skipped")
                continue

            region_offset = region_offset + 5

            # init the layer
            region_img = PIL.Image.new("RGBA", (self.w - self.legend_width, region.size), color=(255, 255, 0, 5))
            region_canvas = PIL.ImageDraw.Draw(region_img)

            # draw the region graphic
            region_canvas.rectangle(
                (0, 0, self.w - 1, region.origin + region.size),
                fill=region.colour,
                outline="black",
                width=1,
            )

            img_main.paste(region_img, (self.legend_width + region_offset, region.origin), region_img)

            # add origin text for the region
            text_img = PIL.Image.new("RGB", (30, 10), color=(255, 255, 0))
            text_canvas = PIL.ImageDraw.Draw(text_img)
            text_canvas.text((0, 0), str(region.origin), fill="black")
            text_img = text_img.rotate(180)
            img_main.paste(text_img, (0, region.origin))

        # horizontal flip and write to file
        img_main = img_main.rotate(180)

        # output image file
        img_file = pathlib.Path(self.args.out).stem + ".png"
        img_main.save(pathlib.Path(self.args.out).parent / img_file)

        # output report
        self._export(region_list)

    def _export(self, region_list: List[mmdiagram.types.Region]):
        with open(self.args.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(self.args.out).stem}.png)\n""")
            f.write("|name|colour|origin|size|remaining|\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for region in region_list:
                f.write(f"{region}\n")

    def _process_input(self) -> List[mmdiagram.types.Region]:

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("regions", help='command line input for regions should be tuples of name, origin and size.', nargs="*")
        self.parser.add_argument("-o", "--out", help='path to the markdown output report file. Defaults to "out/report.md"', default="out/report.md")
        self.args = self.parser.parse_args()

        # make sure the output path is valid and parent dir exists
        if not pathlib.Path(self.args.out).suffix == ".md":
            raise NameError("Output file should end with .md")
        pathlib.Path(self.args.out).parent.mkdir(parents=True, exist_ok=True)

        if len(sys.argv) == 1:
            self.parser.error("must pass in data points")
        if len(self.args.regions) % 3:
            self.parser.error("command line input data should be in multiples of three")

        region_list = []
        for clituple in self._batched(self.args.regions, 3):
            region_list.append(mmdiagram.types.Region(clituple[0], clituple[1], clituple[2]))

        return region_list

    def _batched(self, iterable, n):
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch


if __name__ == "__main__":
    Diagram()
