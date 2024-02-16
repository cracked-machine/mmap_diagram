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
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


@typeguard.typechecked
class MemoryMap:

    class DashedLine:
        width: int = 1
        gap: int = 4
        len: int = gap // 2

    def __init__(self):
        self.bgcolour = "oldlace"
        """background colour for diagram"""

        self.height: int = None
        """height of the diagram image"""

        self.width: int = 400
        """width of the diagram image"""

        self.default_region_text_size: int = 12
        """Default size for memregion text"""

        self.fixed_legend_text_size = 12
        """Fixed size for legend text"""

        self.table_text_size = 15
        """Fixed size for table text"""

        self.void_thres: int = None
        """Void space threshold for adding VoidRegion objs"""

        self._region_list: List[mm.types.MemoryRegion] = []
        """List of memregion objects"""

        self._process_input()

        # attributes using self.width/self.height
        # should be done after this function call
        self._rescale_image()

        self._legend_width = self.width // 2
        """width of the area used for text annotations/legend"""

        self.voidregion = mm.types.VoidRegion(size=hex(40))
        """The reusable object used to represent the void regions in the memory map"""
        self.voidregion.create_img(img_width=(self.width - 20), font_size=self.default_region_text_size)

        self.top_addr_lbl = mm.types.TextLabel(hex(self.height), self.fixed_legend_text_size)
        """Make sure this is created after rescale"""

        # calculate each regions distance to the next memregion and for any overlaps
        memregion: mm.types.MemoryRegion
        for memregion in self._region_list:
            memregion.calc_nearest_region(self._region_list, self.height)

        # assign the draw indent by ascending origin
        self._region_list.sort(key=lambda x: x.origin, reverse=False)
        region_indent = 0
        for memregion in self._region_list:
            memregion.draw_indent = region_indent
            region_indent += 5

        # sort in descending size order for z-order.
        # smaller in foreground, larger in background
        self._region_list.sort(key=lambda x: x.size, reverse=True)

        self._create_diagram_image(self._region_list)
        self._create_markdown(self._region_list)
        self._create_table_image(self._region_list)

    def _rescale_image(self):
        """Rescale the image using the default or user-defined scale factor"""
        self.height = self.height * self.scale_factor
        self.width = self.width * self.scale_factor

    def _create_diagram_image(self, region_list: List[mm.types.MemoryRegion]):
        """Create the png format image for the diagram from the mm.types.MemoryRegion objects"""
        # init the main image
        new_diagram_img = PIL.Image.new("RGB", (self.width, self.height), color=self.bgcolour)

        # paste each new graphic element image to main image
        for memregion in region_list:
            memregion.create_img(
                img_width=(self.width - self._legend_width),
                font_size=self.default_region_text_size,
            )
            if not memregion.img:
                continue
            new_diagram_img.paste(
                memregion.img,
                (self._legend_width + memregion.draw_indent, memregion.origin),
                memregion.img,
            )

            # Origin address text for this memory region
            origin_text_label = mm.types.TextLabel(memregion._origin, self.fixed_legend_text_size)
            new_diagram_img.paste(
                origin_text_label.img,
                (0, memregion.origin - origin_text_label.height + 1),
            )

            # End address text for this memory region
            region_end_addr = memregion.origin + memregion.size
            region_end_addr_lbl = mm.types.TextLabel(hex(region_end_addr), self.fixed_legend_text_size)
            new_diagram_img.paste(
                region_end_addr_lbl.img,
                (0, region_end_addr - region_end_addr_lbl.height + 1),
            )

            # Top address text for the whole diagram
            top_addr = self.height
            top_addr_lbl = mm.types.TextLabel(hex(top_addr), self.fixed_legend_text_size)
            new_diagram_img.paste(top_addr_lbl.img, (0, top_addr - top_addr_lbl.height - 5))

            # Dash Lines from text to memregion
            line_canvas = PIL.ImageDraw.Draw(new_diagram_img)
            for x in range(
                region_end_addr_lbl.width * 2,
                self._legend_width - 10,
                MemoryMap.DashedLine.gap,
            ):
                line_canvas.line(
                    (
                        x,
                        region_end_addr - MemoryMap.DashedLine.width,
                        x + MemoryMap.DashedLine.len,
                        region_end_addr - MemoryMap.DashedLine.width,
                    ),
                    fill="black",
                    width=MemoryMap.DashedLine.width,
                )

            for x in range(
                origin_text_label.width * 2,
                self._legend_width - 10,
                MemoryMap.DashedLine.gap,
            ):
                line_canvas.line(
                    (
                        x,
                        memregion.origin - MemoryMap.DashedLine.width,
                        x + MemoryMap.DashedLine.len,
                        memregion.origin - MemoryMap.DashedLine.width,
                    ),
                    fill="black",
                    width=1,
                )

            for x in range(top_addr_lbl.width * 2, self.width - 10, MemoryMap.DashedLine.gap):
                line_canvas.line(
                    (x, top_addr - 7, x + MemoryMap.DashedLine.len, top_addr - 7),
                    fill="black",
                    width=MemoryMap.DashedLine.width,
                )

        self._insert_void_regions(new_diagram_img, region_list)

        # rotate the entire diagram so the origin is at the bottom
        new_diagram_img = new_diagram_img.rotate(180)

        # output image file
        img_file_path = pathlib.Path(self.args.out).stem + "_full.png"
        new_diagram_img.save(pathlib.Path(self.args.out).parent / img_file_path)

    def _insert_void_regions(self, original_img: PIL.Image.Image, memregion_list: List[mm.types.MemoryRegion]):
        """Remove large empty spaces and replace them with fixed size VoidRegion objects.
        This function actually chops up the existing diagram image into smaller images containing
        only MemoryRegions. It then pastes the smaller image into a new image, inserting VoidRegion
        images inbetween"""

        # find the large empty spaces in the memory map
        region_subset_list: List[PIL.Image.Image] = []
        img_addr_idx = 0
        for memregion in memregion_list:
            region_end_addr = memregion.origin + memregion.size
            if int(memregion.remain, 16) > self.void_threshold:

                # dont forget the image is upside down at this stage, so upper and lower are reversed.
                (left, upper, right, lower) = (
                    0,
                    img_addr_idx - 10,
                    original_img.width,
                    region_end_addr + 10,
                )
                region_subset = original_img.crop((left, upper, right, lower))
                region_subset_list.append(region_subset)

                # move the cursor up past the end of the current memregion and the empty space
                img_addr_idx = region_end_addr + int(memregion.remain, 16)

        if not region_subset_list:
            # no spaces were found in the diagram to be above the void threshold
            img_file_path = pathlib.Path(self.args.out).stem + "_cropped.png"
            original_img = original_img.rotate(180)
            original_img.save(pathlib.Path(self.args.out).parent / img_file_path)
        else:
            # calculate the new reduced diagram image height plus some padding
            new_cropped_height = (
                sum(img.height for img in region_subset_list)
                + (len(region_subset_list) * self.voidregion.img.height)
                + 20
            )

            # now create the new image alternating the region subsets and void regions
            new_cropped_image = PIL.Image.new("RGB", (self.width, new_cropped_height), color=self.bgcolour)
            y_pos = 0
            for region_subset in region_subset_list:
                new_cropped_image.paste(region_subset, (0, y_pos))
                y_pos = y_pos + region_subset.height

                new_cropped_image.paste(self.voidregion.img, (10, y_pos))
                y_pos = y_pos + self.voidregion.img.height

            # Diagram End Address Text
            new_cropped_image.paste(
                self.top_addr_lbl.img,
                (0, new_cropped_image.height - self.top_addr_lbl.height - 10),
            )

            # Diagram End Dash Line
            line_canvas = PIL.ImageDraw.Draw(new_cropped_image)
            for x in range(self.top_addr_lbl.width * 2, self.width - 10, MemoryMap.DashedLine.gap):
                line_canvas.line(
                    (
                        x,
                        new_cropped_image.height - self.top_addr_lbl.height - 3,
                        x + MemoryMap.DashedLine.len,
                        new_cropped_image.height - self.top_addr_lbl.height - 3,
                    ),
                    fill="black",
                    width=MemoryMap.DashedLine.width,
                )

            new_cropped_image = new_cropped_image.rotate(180)
            img_file_path = pathlib.Path(self.args.out).stem + "_cropped.png"
            new_cropped_image.save(pathlib.Path(self.args.out).parent / img_file_path)

    def _create_markdown(self, region_list: List[mm.types.MemoryRegion]):
        """Create markdown doc containing the diagram image and text-base summary table"""
        with open(self.args.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(self.args.out).stem}.png)\n""")
            f.write("|name|origin|size|remaining|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for memregion in region_list:
                f.write(f"{memregion}\n")

    def _create_table_image(self, region_list: List[mm.types.MemoryRegion]):
        """Create a png image of the summary table"""
        table_data = []
        for memregion in reversed(region_list):
            table_data.append(memregion.get_data_as_list())

        table: PIL.Image.Image = mm.types.Table().draw_table(
            table=table_data,
            header=["Name", "Origin", "Size", "Remains", "Collisions"],
            font=PIL.ImageFont.load_default(self.table_text_size),
            stock=True,
            colors={"red": "green", "green": "red"},
        )
        tableimg_file_path = pathlib.Path(self.args.out).stem + "_table.png"
        table.save(pathlib.Path(self.args.out).parent / tableimg_file_path)

    def _process_input(self):

        parser = argparse.ArgumentParser(
            description="""Generate a diagram showing how binary regions co-exist within memory."""
        )
        parser.add_argument(
            "regions",
            help="command line input for regions should be tuples of name, origin and size.",
            nargs="*",
        )
        parser.add_argument(
            "-o",
            "--out",
            help='path to the markdown output report file. Default: "out/report.md"',
            default="out/report.md",
        )
        parser.add_argument(
            "-l",
            "--limit",
            help="The maximum memory address for the diagram. Please use hex. Default: " + hex(1000) + " (1000)",
            default=hex(1000),
            type=str,
        )
        parser.add_argument(
            "-s",
            "--scale",
            help="The scale factor for the diagram. Default: 1",
            default=1,
            type=int,
        )
        parser.add_argument(
            "-v",
            "--voidthreshold",
            help="The threshold for skipping void sections. Please use hex. Default: " + hex(1000) + " (1000)",
            default=hex(1000),
            type=str,
        )

        self.args = parser.parse_args()

        # parse hex/int inputs
        if not self.args.limit[:2] == "0x":
            parser.error("'limit' argument should be in hex format: 0x")
        self.height: int = int(self.args.limit, 16)

        self.scale_factor: int = int(self.args.scale)

        if not self.args.voidthreshold[:2] == "0x":
            parser.error("'voidthreshold' argument should be in hex format: 0x")
        self.void_threshold: int = int(self.args.voidthreshold, 16)

        # make sure the output path is valid and parent dir exists
        if not pathlib.Path(self.args.out).suffix == ".md":
            raise NameError("Output file should end with .md")
        pathlib.Path(self.args.out).parent.mkdir(parents=True, exist_ok=True)

        # check data point cardinality
        if len(sys.argv) == 1:
            parser.error("must pass in data points")
        if len(self.args.regions) % 3:
            parser.error("command line input data should be in multiples of three")

        # create mm.types.MemoryRegion objs for each data tuple
        for datatuple in self._batched(self.args.regions, 3):
            name = datatuple[0]
            origin = datatuple[1]
            size = datatuple[2]
            if not origin[:2] == "0x" or not size[:2] == "0x":
                logging.critical(
                    f"Region 'origin' and 'size' data should be in hex (0x) format: Found {datatuple}",
                )
                raise SystemExit()
            if self._region_list and any(x.name == name for x in self._region_list):
                warnings.warn(
                    f"Duplicate memregion names ({name}) are not permitted. MemoryRegion will not be added.",
                    RuntimeWarning,
                )
            else:
                self._region_list.append(mm.types.MemoryRegion(name, origin, size))

    def _batched(self, iterable, n):
        """batched('ABCDEFG', 3) --> ABC DEF G"""
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch


if __name__ == "__main__":
    MemoryMap()
