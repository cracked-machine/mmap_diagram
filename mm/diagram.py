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

import json

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

        self.voidthreshold: int = int(Diagram.pargs.voidthreshold, 16)
        """Void space threshold for adding VoidRegionImage objs"""


        self.top_addr_lbl = mm.image.TextLabelImage(hex(Diagram.model.diagram_height), self.fixed_legend_text_size)
        """Make sure this is created after rescale"""

        self.final_image_full: PIL.Image.Image = None
        """Final image for this Memory Map - without void regions"""

        self.final_image_reduced: PIL.Image.Image = None
        """Final image for this Memory Map - with void regions"""
        
        assert len(memory_map_metadata) == 1, "MemoryMapDiagram should omly be initialised with a single mm.metamodel.MemoryMap."
        
        self.width = next(iter(memory_map_metadata.values())).map_width
        self.height = next(iter(memory_map_metadata.values())).map_height

        legend_width_pixels = (self.width // 100) * Diagram.model.diagram_legend_width
        self._legend_width = legend_width_pixels
        """width of the area used for text annotations/legend"""

        self.voidregion = mm.image.VoidRegionImage()
        """The reusable object used to represent the void regions in the memory map"""
        self.voidregion.create_img(
            img_width=(self.width - self._legend_width - (self.width//5)), 
            font_size=self.default_region_text_size)
       

        self.image_list = self._create_image_list(memory_map_metadata)


    def _create_image_list(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]) -> List[mm.image.MemoryRegionImage]:
        
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
    
    def _draw_image_list(
            self, 
            image_list: List[mm.image.MemoryRegionImage]):
        
        new_diagram_img = PIL.Image.new(
            "RGB", 
            (self.width, 
             self.height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        # paste each new graphic element image to main image
        for memregion in image_list:
            memregion.create_img(
                img_width=(self.width - self._legend_width - (self.width//5)),
                font_size=self.default_region_text_size,
            )
            if not memregion.img:
                continue
            new_diagram_img.paste(
                memregion.img,
                ((((self.width - memregion.draw_indent - self._legend_width) - memregion.img.width) // 2) + self._legend_width, 
                 int(memregion.origin_as_hex,16)),
                memregion.img,
            )

            # End address text for this memory region
            region_end_addr = int(memregion.origin_as_hex,16) + int(memregion.size_as_hex, 16)
            region_end_addr_lbl = mm.image.TextLabelImage(hex(region_end_addr), self.fixed_legend_text_size)
            new_diagram_img.paste(
                region_end_addr_lbl.img,
                (5, region_end_addr - (region_end_addr_lbl.height // 2) + 1),
            )

            # Dash Lines from text to memregion
            line_canvas = PIL.ImageDraw.Draw(new_diagram_img)
            for x in range(
                region_end_addr_lbl.width + 10,
                self._legend_width,
                MemoryMapDiagram.DashedLine.gap):
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

            # Origin address text for this memory region
            origin_text_label = mm.image.TextLabelImage(memregion.origin_as_hex, self.fixed_legend_text_size)
            new_diagram_img.paste(
                origin_text_label.img,
                (5, int(memregion.origin_as_hex,16) - (origin_text_label.height // 2) + 1 ),
            )

            for x in range(
                origin_text_label.width + 10,
                self._legend_width,
                MemoryMapDiagram.DashedLine.gap):
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



        self._insert_void_regions(new_diagram_img, image_list)

        # rotate the entire diagram so the origin is at the bottom
        self.final_image_full = new_diagram_img.rotate(180)

    def _insert_void_regions(
            self, 
            original_img: PIL.Image.Image, 
            memregion_list: List[mm.image.MemoryRegionImage]):
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
            self.final_image_reduced = original_img

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
                (self.width, new_cropped_height), 
                color=mm.diagram.Diagram.model.diagram_bgcolour)
            
            y_pos = 0
            for region_subset in region_subset_list:
                new_cropped_image.paste(region_subset, (0, y_pos))
                y_pos = y_pos + region_subset.height

                new_cropped_image.paste(
                    self.voidregion.img, 
                    # ((new_cropped_image.width - self.voidregion.img.width) // 2, y_pos)
    
                    (((new_cropped_image.width - self._legend_width - self.voidregion.img.width) // 2) + self._legend_width, y_pos)
                )
                y_pos = y_pos + self.voidregion.img.height

            # Diagram End Address Text
            new_cropped_image.paste(
                self.top_addr_lbl.img,
                (5, new_cropped_image.height - self.top_addr_lbl.height - 10),
            )

            # Diagram End Dash Line
            line_canvas = PIL.ImageDraw.Draw(new_cropped_image)
            for x in range(
                self.top_addr_lbl.width + 10, 
                self._legend_width, 
                MemoryMapDiagram.DashedLine.gap):
                line_canvas.line(
                    (
                        x,
                        new_cropped_image.height - self.top_addr_lbl.height - 5,
                        x + MemoryMapDiagram.DashedLine.len,
                        new_cropped_image.height - self.top_addr_lbl.height - 5,
                    ),
                    fill="black",
                    width=MemoryMapDiagram.DashedLine.width,
                )

            self.final_image_reduced = new_cropped_image

        self.final_image_reduced = self.final_image_reduced.rotate(180)

class Diagram:
    pargs: argparse.Namespace = None
    model = None

    def __init__(self):

        self.mmd_list: List[MemoryMapDiagram] = []
        """ instances of the memory map diagram"""

        self._parse_args()
        self._validate_pargs()
        Diagram.model = self._create_model()

        for mmap_name, mmap in Diagram.model.memory_maps.items():
            self.mmd_list.append(MemoryMapDiagram({mmap_name: mmap}))
            pass

        self._draw_full_img_diagram()
        self._draw_reduced_img_diagram()
        self._create_table_image(self.mmd_list)
        self._create_markdown(self.mmd_list)        

    def _draw_full_img_diagram(self):


        full_diagram_img = PIL.Image.new(
            "RGB", 
            (Diagram.model.diagram_width, Diagram.model.diagram_height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        for idx, mmd in enumerate(self.mmd_list):
            full_diagram_img.paste(
                mmd.final_image_full, 
                (idx * mmd.width, 0))
            
        # Top address text for the whole diagram
        line_canvas = PIL.ImageDraw.Draw(full_diagram_img)
        top_addr = Diagram.model.diagram_height
        top_addr_lbl = mm.image.TextLabelImage(hex(top_addr), mmd.fixed_legend_text_size)
        full_diagram_img = full_diagram_img.rotate(180)
        full_diagram_img.paste(top_addr_lbl.img, (5, top_addr - top_addr_lbl.height - 5))
        full_diagram_img = full_diagram_img.rotate(180)

        for x in range(
            top_addr_lbl.width, 
            mmd.width, 
            MemoryMapDiagram.DashedLine.gap):
            line_canvas.line(
                (x, top_addr - 7, x + MemoryMapDiagram.DashedLine.len, top_addr - 7),
                fill="black",
                width=MemoryMapDiagram.DashedLine.width,
            )

        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_full.png"
        full_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _draw_reduced_img_diagram(self):

        # the original dimension may have shrunk for the 
        # reduced mm diagram due to void region cropping
        # TODO restore original
        self.mmd_list.sort(key=lambda x: x.final_image_reduced.height, reverse=True)
        max_reduced_diagram_height = self.mmd_list[0].final_image_reduced.height
 
        if self.mmd_list[0].final_image_reduced.height > Diagram.model.diagram_height:
            logging.warning(f"The largest reduced memory map exceeds the overal diagram height. Clamping to {Diagram.model.diagram_height}")
            self.mmd_list[0].final_image_reduced.height = Diagram.model.diagram_height
 
        reduced_diagram_img = PIL.Image.new(
            "RGB", 
            (Diagram.model.diagram_width, max_reduced_diagram_height), 
            color=mm.diagram.Diagram.model.diagram_bgcolour)
        
        # maps have been cropped to potentially different sizes. To ensure they 
        # line up at zero on the y-axis we rotate each one 180 deg before pasting 
        # them into the main diagram image. We then need to rotate the main image
        # back 180 deg. Because of this the legend positions are now incorrectly 
        # mirrored on the y-axis, so we need to subtract their x-axis positions 
        # from the main diagram image width(!)
        for idx, mmd in enumerate(self.mmd_list):
            mmd.final_image_reduced = mmd.final_image_reduced.rotate(180)
            reduced_diagram_img.paste(
                mmd.final_image_reduced, 
                ( (idx * mmd.width), 0))
            

        reduced_diagram_img = reduced_diagram_img.rotate(180)
        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_cropped.png"
        reduced_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _create_table_image(self, mmd_list: List[MemoryMapDiagram]):
        """Create a png image of the summary table"""

        table_text_size = 15
        """Fixed size for table text"""
        table_data = []
        
        for region_map_list in mmd_list:
            for memregion in (region_map_list.image_list):
                table_data.append(memregion.get_data_as_list())

        table: PIL.Image.Image = mm.image.Table().draw_table(
            table=table_data,
            header=["Name", "Origin", "Size", "Free Space", "Collisions"],
            font=PIL.ImageFont.load_default(table_text_size),
            stock=True,
            colors={"red": "green", "green": "red"},
        )

        tableimg_file_path = pathlib.Path(Diagram.pargs.out).stem + "_table.png"
        table.save(pathlib.Path(Diagram.pargs.out).parent / tableimg_file_path)

    def _create_markdown(self,  mmd_list: List[MemoryMapDiagram]):
        """Create markdown doc containing the diagram image """
        """and text-base summary table"""
        with open(Diagram.pargs.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(Diagram.pargs.out).stem}_cropped.png)\n""")
            f.write("|name|origin|size|free Space|collisions\n")
            f.write("|:-|:-|:-|:-|:-|\n")
            for region_map_list in mmd_list:
                for memregion in (region_map_list.image_list):            
                    f.write(f"{memregion}\n")

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
        if not Diagram.pargs.file:
            if len(Diagram.pargs.regions) % 3:
                raise SystemExit("command line input data should be in multiples of three") 
        else:
            assert pathlib.Path(Diagram.pargs.file).resolve().exists()

    def _create_model(self) -> mm.metamodel.Diagram:
        
        if Diagram.pargs.file:
            with pathlib.Path(Diagram.pargs.file).resolve().open("r") as fp:
                inputdict = json.load(fp)
        else:
                
            # command line parameters only support one memory map per diagram
            inputdict = {
                "$schema": "../../mm/schema.json",
                "diagram_name": "testd",
                "diagram_height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
                "diagram_width": 400 * Diagram.pargs.scale,
                "memory_maps": { 
                    "singlemm": { 
                        "map_height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
                        "map_width": 400 * Diagram.pargs.scale,
                        "memory_regions": { } # regions added below
                    }
                }
            }

            # start adding mem regions from the command line arg
            for datatuple in self._batched(Diagram.pargs.regions, 3):
                # prevent overwriting duplicates
                if datatuple[0] in inputdict['memory_maps']['singlemm']['memory_regions']:
                    logging.warning(f"{str(datatuple[0])} already exists. Skipping {str(datatuple)}.")
                    continue

                inputdict['memory_maps']['singlemm']['memory_regions'][datatuple[0]] = {
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
 
