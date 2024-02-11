import argparse
import itertools
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont

from typing import List, Tuple
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
        self._rescale()

        # create mm.types.MemoryRegion objs for each data tuple
        t: Tuple
        for t in self._batched(self.args.regions, 3):
            name = t[0]
            origin = t[1]
            size = t[2]
            if not origin[:2] == "0x" or not size[:2] == "0x":
                logging.critical(f"Region 'origin' and 'size' data should be in hex (0x) format: Found {t}", )
                raise SystemExit()
            if self._region_list and any(x.name == name for x in self._region_list):
                warnings.warn(f"Duplicate memregion names ({name}) are not permitted. MemoryRegion will not be added.", RuntimeWarning)
            else:
                self._region_list.append(mm.types.MemoryRegion(name, origin, size))

        # calculate each regions distance to the next memregion and for any overlaps
        r: mm.types.MemoryRegion
        for r in self._region_list:
            r.calc_nearest_region(self._region_list, self.height)

        self._legend_width = self.width // 2
        """width of the area used for text annotations/legend"""

        # temporarily sort by ascending origin attribute and assign the draw indent
        self._region_list.sort(key=lambda x: x.origin, reverse=False)
        region_indent = 0
        for r in self._region_list:
            r.draw_indent = region_indent
            region_indent += 5

        # sort in descending order so largest regions are drawn first in z-order (background)
        self._region_list.sort(key=lambda x: x.size, reverse=True)

        self._generate()
        self._create_summary_table(self._region_list)

    def _generate(self):
        # output image diagram
        self._create_diagram(self._region_list)
        # output markdown report (refs image)
        self._create_markdown(self._region_list)

    def _rescale(self):
        self.height = self.height * self.scale_factor
        self.width = self.width * self.scale_factor
        # self.default_region_text_size = self.default_region_text_size * self.scale_factor

    def _create_diagram(self, region_list: List[mm.types.MemoryRegion]):

        # init the main image
        img_main_full = PIL.Image.new("RGB", (self.width, self.height), color=self.bgcolour)

        # paste each new graphic element image to main image
        for memregion in region_list:

            # Regions
            memregion.create_img(img_width=(self.width - self._legend_width), font_size=self.default_region_text_size)
            if not memregion.img:
                continue
            img_main_full.paste(memregion.img, (self._legend_width + memregion.draw_indent, memregion.origin), memregion.img)

            # Origin Address Text
            origin_text_label = mm.types.TextLabel(memregion._origin, self.fixed_legend_text_size)
            img_main_full.paste(origin_text_label.img, (0, memregion.origin - origin_text_label.height + 1))

            # Region End Address Text
            end_addr_val = memregion.origin + memregion.size
            end_addr_text_label = mm.types.TextLabel(hex(end_addr_val), self.fixed_legend_text_size)
            img_main_full.paste(end_addr_text_label.img, (0, end_addr_val - end_addr_text_label.height + 1))

            # Diagram End Address Text
            diagram_end_addr_val = self.height
            diagram_end_addr_label = mm.types.TextLabel(hex(diagram_end_addr_val), self.fixed_legend_text_size)
            img_main_full.paste(diagram_end_addr_label.img, (0, diagram_end_addr_val - diagram_end_addr_label.height - 5))

            # Dash Lines from text to memregion
            line_width = 1
            line_canvas = PIL.ImageDraw.Draw(img_main_full)
            dash_gap = 4
            dash_len = dash_gap / 2

            for x in range(end_addr_text_label.width * 2, self._legend_width - 10, dash_gap):
                line_canvas.line((x, end_addr_val - line_width, x + dash_len, end_addr_val - line_width), fill="black", width=line_width)

            for x in range(origin_text_label.width * 2, self._legend_width - 10, dash_gap):
                line_canvas.line((x, memregion.origin - line_width, x + dash_len, memregion.origin - line_width), fill="black", width=1)

            for x in range(diagram_end_addr_label.width * 2, self.width - 10, dash_gap):
                line_canvas.line((x, diagram_end_addr_val - 7, x + dash_len, diagram_end_addr_val - 7), fill="black", width=line_width)                

        self._truncate_diagram(img_main_full, region_list)

        # rotate the entire diagram so the origin is at the bottom
        img_main_full = img_main_full.rotate(180)

        # output image file
        img_file_path = pathlib.Path(self.args.out).stem + "_full.png"
        img_main_full.save(pathlib.Path(self.args.out).parent / img_file_path)

    def _truncate_diagram(self, img_to_crop: PIL.Image.Image, memregion_list: List[mm.types.MemoryRegion]):
        """Remove large empty spaces and replace them with fixed size VoidRegion objects"""
        # gather up the clusters of regions divided by large spaces
        memregion_cluster_list = []
        address_cursor = 0
        for memregion in memregion_list:
            end_addr_val = memregion.origin + memregion.size
            if int(memregion.remain, 16) > self.void_threshold:
                # dont forget the image is upside down at this stage, so upper and lower are reversed.
                (left, upper, right, lower) = (0, address_cursor - 10, img_to_crop.width, end_addr_val + 10)
                cropped_img = img_to_crop.crop((left, upper, right, lower))
                memregion_cluster_list.append(cropped_img)

                # move the cursor up past the end of the current memregion and the empty space
                address_cursor = end_addr_val + int(memregion.remain, 16)

        # join all the cropped images together into a smaller main image
        voidregion = mm.types.VoidRegion(size=hex(40))
        voidregion.create_img(img_width=(self.width - 20), font_size=self.default_region_text_size)
        total_cropped_height = sum(r.height for r in memregion_cluster_list)
        total_cropped_height = total_cropped_height + (len(memregion_cluster_list) * voidregion.img.height) + 20
        img_main_cropped = PIL.Image.new("RGB", (self.width, total_cropped_height), color=self.bgcolour)
        y_pos = 0
        for region_cluster in memregion_cluster_list:
            img_main_cropped.paste(region_cluster, (0, y_pos))
            y_pos = y_pos + region_cluster.height

            img_main_cropped.paste(voidregion.img, (10, y_pos))
            y_pos = y_pos + voidregion.img.height
            
        # Diagram End Address Text
        diagram_end_addr_val = self.height
        diagram_end_addr_label = mm.types.TextLabel(hex(diagram_end_addr_val), self.fixed_legend_text_size)
        img_main_cropped.paste(diagram_end_addr_label.img, (0, img_main_cropped.height - diagram_end_addr_label.height - 10))
        
        # Diagram End Dash Line
        line_width = 1
        line_canvas = PIL.ImageDraw.Draw(img_main_cropped)
        dash_gap = 4
        dash_len = dash_gap / 2
        for x in range(diagram_end_addr_label.width * 2, self.width - 10, dash_gap):
            line_canvas.line((x, img_main_cropped.height - diagram_end_addr_label.height - 3,
                             x + dash_len,
                             img_main_cropped.height - diagram_end_addr_label.height - 3),
                             fill="black",
                             width=line_width)

        # no large empty regions were found so just copy in the existing image
        if not memregion_cluster_list:
            img_main_cropped = img_to_crop

        img_main_cropped = img_main_cropped.rotate(180)
        img_file_path = pathlib.Path(self.args.out).stem + "_cropped.png"
        img_main_cropped.save(pathlib.Path(self.args.out).parent / img_file_path)

    def _create_markdown(self, region_list: List[mm.types.MemoryRegion]):
        """Create markdown doc containing the diagram image and text-base summary table"""
        with open(self.args.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(self.args.out).stem}.png)\n""")
            f.write("|name|origin|size|remaining|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for memregion in region_list:
                f.write(f"{memregion}\n")

    def _create_summary_table(self, region_list: List[mm.types.MemoryRegion]):
        """Create a png image of the summary table"""
        table_data = []
        for memregion in region_list:
            table_data.append(memregion.get_data_as_list())

        table: PIL.Image.Image = mm.types.Table().draw_table(
            table=table_data,
            header=["Name", "Origin", "Size", "Remains", "Collisions"],
            font=PIL.ImageFont.load_default(self.table_text_size),
            stock=True,
            colors={'red':'green','green':'red'}
        )
        tableimg_file_path = pathlib.Path(self.args.out).stem + "_table.png"
        table.save(pathlib.Path(self.args.out).parent / tableimg_file_path)

    def _process_input(self):

        self.parser = argparse.ArgumentParser(
            description="""Generate a diagram showing how binary regions co-exist within memory.""")
        self.parser.add_argument("regions", help='command line input for regions should be tuples of name, origin and size.',
                                 nargs="*")
        self.parser.add_argument("-o", "--out", help='path to the markdown output report file. Default: "out/report.md"',
                                 default="out/report.md")
        self.parser.add_argument("-l", "--limit",
                                 help="The maximum memory address for the diagram. Please use hex. Default: " + hex(1000) + " (1000)",
                                 default=hex(1000), type=str)
        self.parser.add_argument("-s", "--scale", help="The scale factor for the diagram. Default: 1",
                                 default=1, type=int)
        self.parser.add_argument("-v", "--voidthreshold",
                                 help="The threshold for skipping void sections. Please use hex. Default: " + hex(1000) + " (1000)",
                                 default=hex(1000), type=str)

        self.args = self.parser.parse_args()

        # parse hex/int inputs
        if not self.args.limit[:2] == "0x":
            self.parser.error("'limit' argument should be in hex format: 0x")
        self.height: int = int(self.args.limit, 16)

        self.scale_factor: int = int(self.args.scale)
        
        if not self.args.voidthreshold[:2] == "0x":
            self.parser.error("'voidthreshold' argument should be in hex format: 0x")        
        self.void_threshold: int = int(self.args.voidthreshold, 16)


        # make sure the output path is valid and parent dir exists
        if not pathlib.Path(self.args.out).suffix == ".md":
            raise NameError("Output file should end with .md")
        pathlib.Path(self.args.out).parent.mkdir(parents=True, exist_ok=True)

        # check data point cardinality
        if len(sys.argv) == 1:
            self.parser.error("must pass in data points")
        if len(self.args.regions) % 3:
            self.parser.error("command line input data should be in multiples of three")

    def _batched(self, iterable, n):
        """ batched('ABCDEFG', 3) --> ABC DEF G """
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch


if __name__ == "__main__":
    d = MemoryMap()

