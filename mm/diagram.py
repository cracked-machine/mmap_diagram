import argparse
import itertools
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
import PIL.ImageChops
import PIL.ImageOps
import json
import typeguard
import sys
import pathlib
import logging
import collections

from typing import List, Dict, Literal, Tuple, DefaultDict

import mm.image
import mm.metamodel

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

@typeguard.typechecked
class MemoryMapDiagram:

    def __init__(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]):

        assert len(memory_map_metadata) == 1, \
            "MemoryMapDiagram should omly be initialised with a single mm.metamodel.MemoryMap."

        self.name = next(iter(memory_map_metadata))

        self.img: PIL.Image.Image = None
        """Final image for this Memory Map"""

        self.width = next(iter(memory_map_metadata.values())).width
        """Map sub-diagram width in pixels. Pre-calculated by pydantic model"""

        self.height = next(iter(memory_map_metadata.values())).height
        """Map sub-diagram height in pixels. Pre-calculated by pydantic model"""

        self.draw_scale = next(iter(memory_map_metadata.values())).draw_scale
        """Map sub-diagram drawing scale denominator. Pre-calculated by pydantic model"""

        self.max_address = next(iter(memory_map_metadata.values())).max_address
        """User-defined (via JSON) or calculated from region data if undefined or smaller than region data"""
        
        self.max_address_calculated: bool = next(iter(memory_map_metadata.values())).max_address_calculated
        """The max address value was calculated from region data"""

        self.addr_col_width_percent = (self.width // 100) * Diagram.model.legend_width
        """width of the area used for text annotations/legend"""

        self.title = mm.image.MapTitleImage(
            self.name + " - scale " + str(self.draw_scale) + ":1", 
            img_width=self.width,
            font_size=Diagram.model.text_size,
            fill_colour=Diagram.model.title_fill_colour,
            line_colour=Diagram.model.title_line_colour)
        """Title graphic for this memory map"""
        
        self.voidregion = mm.image.VoidRegionImage(
            self.name,
            w = (self.width - self.addr_col_width_percent - (self.width//5)), 
            h = (Diagram.model.text_size + 10),
            font_size = Diagram.model.text_size,
            fill_colour = Diagram.model.void_fill_colour,
            line_colour = Diagram.model.void_line_colour)
        """The reusable object used to represent the void regions in the memory map"""       

        self.image_list = self._create_image_list(memory_map_metadata)
        """image objects representing each region in the map. In no particular order."""

    def trim_whitespace(self, img: PIL.Image.Image, max: mm.image.Bbox | None = None, min: mm.image.Bbox | None = None) -> PIL.Image.Image:
        """Detect and remove whitespace from img"""

        # getbbox only returns diff with black borders, not white
        img_inverted = PIL.ImageOps.invert(img.convert("RGB"))
        _bbox = mm.image.Bbox(img_inverted.getbbox())
        
        # keep the left/top whitespace by default
        _bbox.left = _bbox.top = 0

        # override the default trim here
        if max:
            if _bbox.left > max.left: _bbox.left = max.left
            if _bbox.top > max.top: _bbox.top = max.top
            if _bbox.right > max.right: _bbox.right = max.right
            if _bbox.bottom > max.bottom: _bbox.bottom = max.bottom

        if min:
            if _bbox.left < min.left: _bbox.left = min.left
            if _bbox.top < min.top: _bbox.top = min.top
            if _bbox.right < min.right: _bbox.right = min.right
            if _bbox.bottom < min.bottom: _bbox.bottom = min.bottom

        return img.crop(_bbox.tuple())

    def _create_image_list(
            self, 
            memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]) -> List[mm.image.MemoryRegionImage]:
        
        image_list: List[mm.image.MemoryRegionImage] = []
        
        mmap_name = next(iter(memory_map_metadata))
        for region_name, region in memory_map_metadata.get(mmap_name).memory_regions.items():
            new_mr_image = mm.image.MemoryRegionImage(
                name=region_name,
                mmap_parent=self.name,
                metadata=region,
                img_width=(self.width - self.addr_col_width_percent - (self.width//5)),
                font_size=region.text_size,
                draw_scale=self.draw_scale
            )
            image_list.append(new_mr_image)
            
        # assign the draw indent by ascending origin
        image_list.sort(key=lambda x: x.origin_as_int, reverse=False)
        region_indent = 0
        if Diagram.model.indent_scheme == "inline":
            pass

        if Diagram.model.indent_scheme == "alternate":
            prev_indent = False
            for image in image_list:
                if image.collisions:
                    image.draw_indent = region_indent
                    if not prev_indent:
                        region_indent = 5
                        prev_indent = True
                    else:
                        region_indent = 0
                        prev_indent = False

        if Diagram.model.indent_scheme == "linear":
            for image in image_list:
                if image.collisions:
                    image.draw_indent = region_indent
                    region_indent += 5
        
        self._create_mmap(image_list, self.draw_scale)   

        return image_list
    

    def _add_label(
            self, 
            dest: PIL.Image, 
            xy: mm.image.Point, 
            text: str, 
            font_size: int,
            y_origin: Literal["top", "bottom"] = "top"
            ) -> PIL.Image.Image:
        """
        Add text to the dest image
        
        - y_origin: draw label with the y-axis origin at the 'top' or 'bottom' edge of the image.
        """

        label = mm.image.TextLabelImage(self.name, text, font_size)

        if y_origin == "bottom":
            xy.y = xy.y - label.height
            return label.overlay(dest, xy)
        else:
            return label.overlay(dest, xy)
        

    def _create_mmap(self, only_memregion_list: List[mm.image.MemoryRegionImage], draw_scale: int) -> None:
        """Create a dict of region groups, interleaved with void regions. 
        Then draw the regions onto a larger memory map image. """

        mixed_region_dict_idx = 0
        mixed_region_dict: DefaultDict = collections.defaultdict(list)

        for memregion in only_memregion_list:
            # start adding memregions to the current subgroup...
            mixed_region_dict[mixed_region_dict_idx].append(memregion)
            # until we hit a empty space larger than the threshold setting
            if memregion.freespace_as_int > Diagram.model.threshold:
                # add a single void region subgroup at a new index...
                mixed_region_dict_idx = mixed_region_dict_idx + 1
                mixed_region_dict[mixed_region_dict_idx].append(self.voidregion)
                # then increment again, ready for next memregion subgroup
                mixed_region_dict_idx = mixed_region_dict_idx + 1

        map_img = PIL.Image.new(
            "RGBA", 
            (self.width, self.height), 
            color=Diagram.model.bgcolour)
        
        next_void_pos = 0
        last_void_pos = 0 
        void_padding = 10
        for group_idx in range(0, len(mixed_region_dict)):

            region: mm.image.MemoryRegionImage
            for region in mixed_region_dict[group_idx]:
                
                if isinstance(region, mm.image.MemoryRegionImage):
                    # adjusted values for drawing ypos - labels should use the original values
                    region_origin_scaled  = region.origin_as_int // draw_scale

                    # add memory region after ypos of last voidregion - if any
                    map_img = region.overlay(
                        dest=map_img, 
                        xy=mm.image.Point(0, last_void_pos if last_void_pos else region_origin_scaled), 
                        alpha=int(Diagram.model.region_alpha))
                    
                    # add origin address text
                    map_img = self._add_label(
                        dest=map_img, 
                        xy=mm.image.Point(region.img.width + 5, (last_void_pos if last_void_pos else region_origin_scaled) - 2 ) , 
                        text=f"0x{region.origin_as_int:X}" + " (" + f"{region.origin_as_int:,}" + ")", 
                        font_size=region.metadata.address_text_size)
                    
                    # ready the ypos for drawing a void region - if any - after this memregion
                    next_void_pos = (last_void_pos if last_void_pos else region_origin_scaled) + (region.img.height) + void_padding

                if isinstance(region, mm.image.VoidRegionImage):
                    # add void region
                    map_img.paste(region.img, (0, next_void_pos))
                    # reset the ypos for the next memregion
                    last_void_pos = next_void_pos + region.img.height + void_padding

        last_region = mixed_region_dict[len(mixed_region_dict) - 1][-1]
        if isinstance(last_region, mm.image.VoidRegionImage):
            map_img = self._add_label(
                dest=map_img, 
                xy=mm.image.Point(last_region.img.width + 5, next_void_pos + last_region.img.height), 
                text=f"0x{self.max_address:X}" + " (" + f"{self.max_address:,}" + ")", 
                font_size=Diagram.model.address_text_size,
                y_origin="bottom")
            
        if isinstance(last_region, mm.image.MemoryRegionImage):
            map_img = self._add_label(
                dest=map_img, 
                xy=mm.image.Point(last_region.img.width + 5, next_void_pos - void_padding), 
                text=f"0x{self.max_address:X}" + " (" + f"{self.max_address:,}" + ")", 
                font_size=last_region.metadata.address_text_size,
                y_origin="bottom")

        min_bbox = None
        if not Diagram.pargs.trim_whitespace:
            min_bbox = mm.image.Bbox((0,0, Diagram.model.width,Diagram.model.height))             
        map_img = self.trim_whitespace(
            map_img, 
            min=min_bbox
        )

        # flip back up the right way
        self.img = map_img.transpose(PIL.Image.FLIP_TOP_BOTTOM)           
        

class Diagram:
    
    pargs: argparse.Namespace = None
    """Command line arguments"""
    model: mm.metamodel.Diagram = None
    """Parsed metamodel from user input json file or
       command line 'region' argument"""

    def __init__(self):
        

        self.mmd_list: List[MemoryMapDiagram] = []
        """ instances of the memory map diagram"""

        Diagram._parse_args()
        Diagram._validate_pargs()
        Diagram.model = Diagram._create_model()

        logging.info(f"Selected diagram height: {str(Diagram.model.height)}")
        logging.info(f"Selected diagram void threshold: {str(Diagram.model.threshold)}")

        # Create the individual memory map diagrams (full and reduced)
        for mmap_name, mmap in Diagram.model.memory_maps.items():
            self.mmd_list.append(MemoryMapDiagram({mmap_name: mmap}))
            pass

        # composite the memory map diagrams into single diagram
        self.draw_diagram_img()

        self._create_table_image(self.mmd_list)
        self._create_markdown(self.mmd_list)        

    def draw_diagram_img(self) -> None:
        """add each memory map to the complete diagram image"""

        max_map_img_height = max(self.mmd_list, key=lambda mmd: mmd.img.height).img.height
        max_title_img_height = max(self.mmd_list, key=lambda mmd: mmd.title.img.height).title.img.height
        
        final_diagram_img = PIL.Image.new(
            "RGBA", 
            (Diagram.model.width, max_map_img_height + max_title_img_height + 10), 
            color=Diagram.model.bgcolour)       
        
        # add region and labels first
        for mmd_idx, mmd in enumerate(self.mmd_list):
            
            # add the mem map diagram image
            final_diagram_img.paste(
                mmd.img.transpose(PIL.Image.FLIP_TOP_BOTTOM), 
                ( (mmd_idx * mmd.width), 0))
            
            # add the mem map name label at this stage so all titles line up at the "top"
            final_diagram_img = mmd.title.overlay(
                final_diagram_img,
                mm.image.Point( (mmd_idx * mmd.width), final_diagram_img.height - max_title_img_height),
                alpha=255)    

        # iterate each memory map -> memory region -> link
        for source_mmd_idx, mmd in enumerate(self.mmd_list):    
            for region_image in mmd.image_list:
                source_region_mid_pos_x = region_image.abs_mid_pos.x
                source_region_mid_pos_y = region_image.abs_mid_pos.y
                for link in region_image.metadata.links:
                    mmd_parent_name = link[0]
                    region_child_name = link[1]
                    # search for the memory map/memory region pair that matches this link
                    for target_mmd_idx, mmd in enumerate(self.mmd_list):
                        if mmd.name == mmd_parent_name:
                            for target_region in mmd.image_list:
                                if target_region.name == region_child_name:
                                    padding = 5
                                    # determine which side of the region block we are drawing to/from
                                    if source_mmd_idx < target_mmd_idx:
                                        source_justify = (region_image.img.width // 2) + padding
                                    else:
                                        source_justify = -(region_image.img.width // 2) - padding

                                    if target_mmd_idx < source_mmd_idx:
                                        target_justify = (target_region.img.width // 2) + padding
                                    else:
                                        target_justify = -(target_region.img.width // 2) - padding                       

                                    # create the link image for the src/dst vector (calc length and angle)           
                                    arrow = mm.image.ArrowBlock(
                                        src = mm.image.Point(
                                            (source_mmd_idx * mmd.width) + source_region_mid_pos_x + source_justify,
                                            source_region_mid_pos_y
                                        ),
                                        dst = mm.image.Point(
                                            (target_mmd_idx * mmd.width) + target_region.abs_mid_pos.x + target_justify, 
                                            target_region.abs_mid_pos.y
                                        ),
                                        head_width = Diagram.model.link_head_width,
                                        tail_len = Diagram.model.link_tail_len,
                                        tail_width = Diagram.model.link_tail_width,
                                        fill = Diagram.model.link_fill_colour,
                                        line = Diagram.model.link_line_colour
                                    )

                                    # add it to the memory map diagram image
                                    final_diagram_img = arrow.overlay(final_diagram_img, mm.image.Point(arrow.pos.x, arrow.pos.y), Diagram.model.link_alpha)
     

        # finalise diagram                                                 
        final_diagram_img = final_diagram_img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        # make sure we don't go over the requested height
        if final_diagram_img.height > Diagram.model.height:
            final_diagram_img = final_diagram_img.resize((Diagram.model.width, Diagram.model.height), PIL.Image.Resampling.BICUBIC)
        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_diagram.png"
        final_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _create_table_image(self, mmd_list: List[MemoryMapDiagram]) -> None:
        """Create a png image of the summary table"""

        table_data = []
        for region_map_list in mmd_list:
            for memregion in (region_map_list.image_list):
                table_data.append(memregion)

        # sort by origin value, then expand into list of lists
        table_data.sort(key=lambda x: x.origin_as_int, reverse=True)
        table_data = [d.get_data_as_list() for d in table_data]

        # Create the table image
        table_img = mm.image.Table().get_table_img(
            table=table_data,
            header=["Region (Parent)", "Origin", "Size", "Free Space", "Collisions", "links", "Drawing Scale"],
            font=PIL.ImageFont.load_default(15),
            stock=True,
            colors={"red": "green", "green": "red"},
        )

        # create the caption image
        
        caption = ""
        for mmd in mmd_list:
            max_address_hex = f"0x{mmd.max_address:X}"
            caption += f"{mmd.name}:"
            caption += f"\n{'':10}max address = 0x{mmd.max_address:X} ({mmd.max_address:,})"
            caption += f"\n{'':10}{'Calculated from region data' if mmd.max_address_calculated else 'User-defined input'}\n"
         
        _, ctop, _, cbottom = PIL.ImageDraw.Draw(PIL.Image.new("RGBA", (0,0))).multiline_textbbox(
            (0,0),
            text=caption,
            font=PIL.ImageFont.load_default(15)
        )              
        caption_img = PIL.Image.new("RGBA", (table_img.width - 20, cbottom - ctop + 15), color="lightgrey")
        PIL.ImageDraw.Draw(caption_img).text((5,5), caption, fill="black", font=PIL.ImageFont.load_default(15))

        # composite the table and cpation images together
        final_table_img = PIL.Image.new("RGBA", (max(caption_img.width, table_img.width), caption_img.height + table_img.height + 30), color="white")
        final_table_img.paste(table_img, (0,0))
        final_table_img.paste(caption_img, (10,table_img.height + 10))

        tableimg_file_path = pathlib.Path(Diagram.pargs.out).stem + "_table.png"
        final_table_img.save(pathlib.Path(Diagram.pargs.out).parent / tableimg_file_path)

    def _create_markdown(self,  mmd_list: List[MemoryMapDiagram]) -> None:
        """Create markdown doc containing the diagram image """
        """and text-base summary table"""
        table_list: List[mm.image.MemoryRegionImage] = []
        for region_map_list in mmd_list:
            for memregion in (region_map_list.image_list): 
                table_list.append(memregion)           

        # sort by ascending origin value starting from the table bottom
        table_list.sort(key=lambda x: x.origin_as_int, reverse=True)

        with open(Diagram.pargs.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(Diagram.pargs.out).stem}_diagram.png)\n""")
            f.write("|region (parent)|origin|size|free Space|collisions|links|draw scale|\n")
            f.write("|:-|:-|:-|:-|:-|:-|:-|\n")
            # use __str__ from mm.image.MemoryRegionImage to print tabulated row
            for mr in table_list:
                f.write(f"{mr}\n")
            f.write("\n---")
            for mmd in mmd_list:
                f.write(f"\n#### {mmd.name}:")
                f.write(f"\n- max address = 0x{mmd.max_address:X} ({mmd.max_address:,})")
                f.write(f"\n- {'Calculated from region data' if mmd.max_address_calculated else 'User-defined input'}")

    @classmethod
    def _parse_args(cls):
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
            help="""
            The 'height' in pixels and 'max address' in bytes for the diagram. 
            Please use hex format. Ignored when using JSON file input.
            Memory regions exceeding this value will be scaled to fit. 
            If you need to set 'height' and 'max address' to different values, 
            please use the JSON input file instead.""",
            type=str
        )
        parser.add_argument(
            "-t",
            "--threshold",
            help="The threshold for skipping void sections. Please use hex.",
            type=str,
            default=hex(200)
        )
        parser.add_argument(
            "-n",
            "--name",
            help="Provide a name for the memory map. Ignored when JSON file is provided.",
            type=str,
        )
        parser.add_argument(
            "-f",
            "--file",
            help="JSON input file for multiple memory maps (and links) support. Please see doc/example/input.json for help.",
            type=str,
        )
        parser.add_argument(
            "-v",
            help="Enable debug output.",
            action="store_true"
        )        
        parser.add_argument(
            "--trim_whitespace",
            help="Force whitespace trim in diagram images.",
            action="store_true"
        )        

        Diagram.pargs = parser.parse_args()

    @classmethod
    def _validate_pargs(cls):
        """"Validate the command line arguments"""
        if Diagram.pargs.v:
            root.setLevel(logging.DEBUG)
        # parse hex/int inputs
        if not Diagram.pargs.file and not Diagram.pargs.limit:
            raise SystemExit("You must specify either: limit setting or JSON input file.")
        if not Diagram.pargs.file and Diagram.pargs.limit:
            if not Diagram.pargs.limit[:2] == "0x":
                raise SystemExit(f"'limit' argument should be in hex format: {str(Diagram.pargs.limit)} = {hex(int(Diagram.pargs.limit))}")
        if not Diagram.pargs.file and not Diagram.pargs.regions:
            raise SystemExit("You must provide either: region string or JSON input file.")
        if Diagram.pargs.threshold:
            if not Diagram.pargs.threshold[:2] == "0x":
                raise SystemExit(f"'threshold' argument should be in hex format: {str(Diagram.pargs.threshold)} = {hex(int(Diagram.pargs.threshold))}")

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
            json_file = pathlib.Path(Diagram.pargs.file).resolve()
            if not json_file.exists():
                raise SystemExit(f"File not found: {json_file}")
    
    @classmethod
    def _create_model(cls) -> mm.metamodel.Diagram:
        
        if Diagram.pargs.file:
            if Diagram.pargs.limit:
                logging.warning("Limit flag is ignore when using JSON input. Using the JSON file Diagram -> height field instead.")
            with pathlib.Path(Diagram.pargs.file).resolve().open("r") as fp:
                inputdict = json.load(fp)
        else:
            mmname = Diagram.pargs.name if Diagram.pargs.name else "Untitled"
            # command line parameters only support one memory map per diagram
            inputdict = {
                "$schema": "../../mm/schema.json",
                "name": "Diagram",
                "height": int(Diagram.pargs.limit,16),
                "width": 400,
                "threshold": int(Diagram.pargs.threshold, 16),
                "memory_maps": { 
                    mmname : { 
                        "max_address": int(Diagram.pargs.limit,16),
                        "height": int(Diagram.pargs.limit,16),
                        "width": 400,
                        "memory_regions": { } # regions added below
                    }
                }
            }

            # start adding mem regions from the command line arg
            for datatuple in Diagram._batched(Diagram.pargs.regions, 3):
                # prevent overwriting duplicates
                if datatuple[0] in inputdict['memory_maps'][mmname]['memory_regions']:
                    logging.warning(f"{str(datatuple[0])} already exists. Skipping {str(datatuple)}.")
                    continue

                inputdict['memory_maps'][mmname]['memory_regions'][datatuple[0]] = {
                        "origin": datatuple[1],
                        "size": datatuple[2]
                    }
            
        return mm.metamodel.Diagram(**inputdict)

    @classmethod
    def _batched(cls, iterable, n):
        """Split iterable into batches"""
        """batched('ABCDEFG', 3) --> ABC DEF G"""
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch

if __name__ == "__main__":
    Diagram()
 
