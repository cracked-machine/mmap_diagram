import argparse
import itertools

import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont

from typing import List, Dict
import typeguard

import sys
import pathlib
import logging

import mm.image
import mm.metamodel

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


@typeguard.typechecked
class MemoryMapDiagram:

    class DashedLine:
        width: int = 1
        gap: int = 4
        len: int = gap // 2

    def __init__(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]):

        # self.bgcolour = "oldlace"
        # """background colour for diagram"""

        self.default_region_text_size: int = 12
        """Default size for memregion text"""

        self.fixed_legend_text_size = 12
        """Fixed size for legend text"""

        self.table_text_size = 15
        """Fixed size for table text"""

        self.voidthreshold: int = int(Diagram.pargs.voidthreshold, 16)
        """Void space threshold for adding VoidRegionImage objs"""

        self._legend_width = Diagram.model.diagram_width // 2
        """width of the area used for text annotations/legend"""

        self.voidregion = mm.image.VoidRegionImage()
        """The reusable object used to represent the void regions in the memory map"""
        self.voidregion.create_img(img_width=(Diagram.model.diagram_width - 20), font_size=self.default_region_text_size)

        self.top_addr_lbl = mm.image.TextLabelImage(hex(Diagram.model.diagram_height), self.fixed_legend_text_size)
        """Make sure this is created after rescale"""

        self.final_image_full: PIL.Image.Image = None
        """Final image for this Memory Map - without void regions"""

        self.final_image_reduced: PIL.Image.Image = None
        """Final image for this Memory Map - with void regions"""

        self.image_list = self._create_image_list(memory_map_metadata)
        self._create_markdown(self.image_list)
        self._create_table_image(self.image_list)

    def _create_image_list(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]) -> List[mm.image.MemoryRegionImage]:

        assert len(memory_map_metadata) == 1, "MemoryMapDiagram should omly be initialised with a single mm.metamodel.MemoryMap."
        
        image_list: List[mm.image.MemoryRegionImage] = []
    
        mmap_name = next(iter(memory_map_metadata))
        for region_name in memory_map_metadata[mmap_name].memory_regions.keys():
            new_mr_image = mm.image.MemoryRegionImage(
                mmap_name,
                region_name
            )
            image_list.append(new_mr_image)
            

        # assign the draw indent by ascending origin
        image_list.sort(key=lambda x: x.origin_as_int, reverse=False)
        region_indent = 0
        for image in image_list:
            image.draw_indent = region_indent
            region_indent += 5

        # sort in descending size order for z-order.
        # smaller in foreground, larger in background
        image_list.sort(key=lambda x: x.size_as_int, reverse=True)
    
        self._draw_image_list(image_list)

        return image_list
    
    def _draw_image_list(self, image_list: List[mm.image.MemoryRegionImage]):

        new_diagram_img = PIL.Image.new(
            "RGB", 
            (Diagram.model.diagram_width, Diagram.model.diagram_height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        # paste each new graphic element image to main image
        for memregion in image_list:
            memregion.create_img(
                img_width=(Diagram.model.diagram_width - self._legend_width),
                font_size=self.default_region_text_size,
            )
            if not memregion.img:
                continue
            new_diagram_img.paste(
                memregion.img,
                (self._legend_width + memregion.draw_indent, int(memregion.origin_as_hex,16)),
                memregion.img,
            )

            # Origin address text for this memory region
            origin_text_label = mm.image.TextLabelImage(
                memregion.origin_as_hex, self.fixed_legend_text_size)
            new_diagram_img.paste(
                origin_text_label.img,
                (0, int(memregion.origin_as_hex,16) - origin_text_label.height + 1),
            )

            # End address text for this memory region
            region_end_addr = int(memregion.origin_as_hex,16) + int(memregion.size_as_hex, 16)
            region_end_addr_lbl = mm.image.TextLabelImage(hex(region_end_addr), self.fixed_legend_text_size)
            new_diagram_img.paste(
                region_end_addr_lbl.img,
                (0, region_end_addr - region_end_addr_lbl.height + 1),
            )

            # Top address text for the whole diagram
            top_addr = Diagram.model.diagram_height
            top_addr_lbl = mm.image.TextLabelImage(hex(top_addr), self.fixed_legend_text_size)
            new_diagram_img.paste(top_addr_lbl.img, (0, top_addr - top_addr_lbl.height - 5))

            # Dash Lines from text to memregion
            line_canvas = PIL.ImageDraw.Draw(new_diagram_img)
            for x in range(
                region_end_addr_lbl.width * 2,
                self._legend_width - 10,
                MemoryMapDiagram.DashedLine.gap,
            ):
                line_canvas.line(
                    (
                        x,
                        region_end_addr - MemoryMapDiagram.DashedLine.width,
                        x + MemoryMapDiagram.DashedLine.len,
                        region_end_addr - MemoryMapDiagram.DashedLine.width,
                    ),
                    fill="black",
                    width=MemoryMapDiagram.DashedLine.width,
                )

            for x in range(
                origin_text_label.width * 2,
                self._legend_width - 10,
                MemoryMapDiagram.DashedLine.gap,
            ):
                line_canvas.line(
                    (
                        x,
                        int(memregion.origin_as_hex, 16) - MemoryMapDiagram.DashedLine.width,
                        x + MemoryMapDiagram.DashedLine.len,
                        int(memregion.origin_as_hex,16) - MemoryMapDiagram.DashedLine.width,
                    ),
                    fill="black",
                    width=1,
                )

            for x in range(top_addr_lbl.width * 2, Diagram.model.diagram_width - 10, MemoryMapDiagram.DashedLine.gap):
                line_canvas.line(
                    (x, top_addr - 7, x + MemoryMapDiagram.DashedLine.len, top_addr - 7),
                    fill="black",
                    width=MemoryMapDiagram.DashedLine.width,
                )

        self._insert_void_regions(new_diagram_img, image_list)

        # rotate the entire diagram so the origin is at the bottom
        self.final_image_full = new_diagram_img.rotate(180)

    def _insert_void_regions(self, original_img: PIL.Image.Image, memregion_list: List[mm.image.MemoryRegionImage]):
        """Remove large empty spaces and replace them with fixed size VoidRegionImage objects.
        This function actually chops up the existing diagram image into smaller images containing
        only MemoryRegions. It then pastes the smaller image into a new image, inserting VoidRegionImage
        images inbetween"""

        # find the large empty spaces in the memory map
        region_subset_list: List[PIL.Image.Image] = []
        img_addr_idx = 0
        # TODO sort memregion_list by ascending
        # memregion_list.sort(key=lambda x: x.size_as_hex, reverse=True)
        for memregion in memregion_list:
            region_end_addr = memregion.origin_as_int + memregion.size_as_int
            if memregion.freespace_as_int > self.voidthreshold:

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
                img_addr_idx = region_end_addr + memregion.freespace_as_int

        if not region_subset_list:
            # no spaces were found in the diagram to be above the void threshold
            self.final_image_reduced = original_img.rotate(180)

        else:
            # calculate the new reduced diagram image height plus some padding
            new_cropped_height = (
                sum(img.height for img in region_subset_list)
                + (len(region_subset_list) * self.voidregion.img.height)
                + 20
            )

            # now create the new image alternating the region subsets and void regions
            new_cropped_image = PIL.Image.new(
                "RGB", 
                (Diagram.model.diagram_width, new_cropped_height), 
                color=mm.diagram.Diagram.model.diagram_bgcolour)
            
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
            for x in range(self.top_addr_lbl.width * 2, Diagram.model.diagram_width - 10, MemoryMapDiagram.DashedLine.gap):
                line_canvas.line(
                    (
                        x,
                        new_cropped_image.height - self.top_addr_lbl.height - 3,
                        x + MemoryMapDiagram.DashedLine.len,
                        new_cropped_image.height - self.top_addr_lbl.height - 3,
                    ),
                    fill="black",
                    width=MemoryMapDiagram.DashedLine.width,
                )

            # TODO disable save and store in class instance variable
            self.final_image_reduced = new_cropped_image.rotate(180)

    def _create_markdown(self, region_list: List[mm.image.MemoryRegionImage]):
        """Create markdown doc containing the diagram image and text-base summary table"""
        with open(Diagram.pargs.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(Diagram.pargs.out).stem}.png)\n""")
            f.write("|name|origin|size|free Space|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for memregion in region_list:
                f.write(f"{memregion}\n")

    def _create_table_image(self, region_list: List[mm.image.MemoryRegionImage]):
        """Create a png image of the summary table"""
        table_data = []
        for memregion in reversed(region_list):
            table_data.append(memregion.get_data_as_list())

        table: PIL.Image.Image = mm.image.Table().draw_table(
            table=table_data,
            header=["Name", "Origin", "Size", "Free Space", "Collisions"],
            font=PIL.ImageFont.load_default(self.table_text_size),
            stock=True,
            colors={"red": "green", "green": "red"},
        )

        # TODO disable save and store in class instance variable
        tableimg_file_path = pathlib.Path(Diagram.pargs.out).stem + "_table.png"
        table.save(pathlib.Path(Diagram.pargs.out).parent / tableimg_file_path)

class Diagram:
    pargs: argparse.Namespace = None
    

    def __init__(self):

        self.mmd_list: List[MemoryMapDiagram] = []
        """ instances of the memory map diagram"""

        self._parse_args()
        self._validate_pargs()
        Diagram.model = self._create_model()

        self._draw_full_img_diagram()
        self._draw_reduced_img_diagram()

    def _draw_full_img_diagram(self):

        for mmap_name, mmap in Diagram.model.memory_maps.items():
            self.mmd_list.append(MemoryMapDiagram({mmap_name: mmap}))

        full_diagram_img = PIL.Image.new(
            "RGB", 
            (Diagram.model.diagram_width, Diagram.model.diagram_height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        for mmd in self.mmd_list:
            full_diagram_img.paste(
                mmd.final_image_full, 
                (0, 0))

        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_full.png"
        full_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _draw_reduced_img_diagram(self):

        # the original dimension may have shrunk for the 
        # reduced mm diagram due to void region cropping
        max_reduced_diagram_height = Diagram.model.diagram_height
        max_reduced_diagram_width = Diagram.model.diagram_width
        for mmd in self.mmd_list:
            if mmd.final_image_reduced.height < max_reduced_diagram_height:
                max_reduced_diagram_height = mmd.final_image_reduced.height
            if mmd.final_image_reduced.width < max_reduced_diagram_width:
                max_reduced_diagram_width = mmd.final_image_reduced.width

        reduced_diagram_img = PIL.Image.new(
            "RGB", 
            (max_reduced_diagram_width, max_reduced_diagram_height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        for mmd in self.mmd_list:
            reduced_diagram_img.paste(
                mmd.final_image_reduced, 
                (0, 0))

        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_cropped.png"
        reduced_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _parse_args(self):
        """Setup the command line interface"""
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

        parser.add_argument(
            "-f",
            "--file",
            help="JSON input file for multiple memory maps (and links) support. Please see doc/example/input.json for help.",
            type=str,
        )

        Diagram.pargs = parser.parse_args()

    def _validate_pargs(self):
        """"Validate the command line arguments"""
        # parse hex/int inputs
        if not Diagram.pargs.limit[:2] == "0x":
            raise SystemExit("'limit' argument should be in hex format: 0x")
 
        if not Diagram.pargs.voidthreshold[:2] == "0x":
            raise SystemExit("'voidthreshold' argument should be in hex format: 0x")

        # make sure the output path is valid and parent dir exists
        if not pathlib.Path(Diagram.pargs.out).suffix == ".md":
            raise NameError("Output file should end with .md")
        pathlib.Path(Diagram.pargs.out).parent.mkdir(parents=True, exist_ok=True)

        # check data point cardinality
        if len(sys.argv) == 1:
            raise SystemExit("must pass in data points")
        if len(Diagram.pargs.regions) % 3:
            raise SystemExit("command line input data should be in multiples of three") 

    def _create_model(self) -> mm.metamodel.Diagram:
        # TODO implement multi- memory map support (only single mm for now)

        # Create the minimal empty dict 
        inputdict = {
            "$schema": "../../mm/schema.json",
            "diagram_name": "testd",
            "diagram_height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
            "diagram_width": 400 * Diagram.pargs.scale,
            "memory_maps": { 
                "testmm": { 
                    "map_height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
                    "map_width": 400 * Diagram.pargs.scale,
                    "memory_regions": { } # regions added below
                }
            }
        }

        # start adding mem regions from the command line arg
        for datatuple in self._batched(Diagram.pargs.regions, 3):
            # prevent overwriting duplicates
            if datatuple[0] in inputdict['memory_maps']['testmm']['memory_regions']:
                logging.warning(f"{str(datatuple[0])} already exists. Skipping {str(datatuple)}.")
                continue

            inputdict['memory_maps']['testmm']['memory_regions'][datatuple[0]] = {
                    "memory_region_origin": datatuple[1],
                    "memory_region_size": datatuple[2]
                }
            
        return mm.metamodel.Diagram(**inputdict)

    def _batched(self, iterable, n):
        """Split iterable into batches"""
        """batched('ABCDEFG', 3) --> ABC DEF G"""
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch

if __name__ == "__main__":
    Diagram()
 
