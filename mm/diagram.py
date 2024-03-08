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

from typing import List, Dict

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

    def __init__(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]):

        assert len(memory_map_metadata) == 1, \
            "MemoryMapDiagram should omly be initialised with a single mm.metamodel.MemoryMap."

        self.name = next(iter(memory_map_metadata))

        self.voidthreshold: int = int(Diagram.pargs.voidthreshold, 16)
        """Void space threshold for adding VoidRegionImage objs"""

        self.final_map_img_redux: PIL.Image.Image = None
        """Final image for this Memory Map"""

        self.width = next(iter(memory_map_metadata.values())).width
        """Map sub-diagram width in pixels. Pre-calculated by pydantic model"""

        self.height = next(iter(memory_map_metadata.values())).height
        """Map sub-diagram height in pixels. Pre-calculated by pydantic model"""

        self.draw_scale = next(iter(memory_map_metadata.values())).draw_scale
        """Map sub-diagram drawing scale denominator. Pre-calculated by pydantic model"""

        self.addr_col_width_percent = (self.width // 100) * Diagram.model.legend_width
        """width of the area used for text annotations/legend"""

        self.name_lbl = mm.image.MapNameImage(
            self.name + " - scale " + str(self.draw_scale) + ":1", 
            img_width=self.width, 
            font_size=Diagram.model.text_size,
            fill_colour=Diagram.model.title_fill_colour,
            line_colour=Diagram.model.title_line_colour)
        """Title graphic for this memory map"""
        
        self.voidregion = mm.image.VoidRegionImage(
            self.name,
            img_width=(self.width - self.addr_col_width_percent - (self.width//5)), 
            font_size=Diagram.model.text_size,
            fill_colour=Diagram.model.void_fill_colour,
            line_colour=Diagram.model.void_line_colour)
        """The reusable object used to represent the void regions in the memory map"""       

        self.image_list = self._create_image_list(memory_map_metadata)

    def trim_whitespace(self, img: PIL.Image.Image) -> PIL.Image.Image:
        """Detect and remove whitespace from img"""

        img_inverted = PIL.ImageOps.invert(img.convert("RGB"))
        bbox = img_inverted.getbbox()
        adjusted_bbox = list(bbox)
        adjusted_bbox[0] = adjusted_bbox[1] = 0
        bbox = tuple(adjusted_bbox)
        return img.crop(bbox)

    def _create_image_list(self, memory_map_metadata: Dict[str, mm.metamodel.MemoryMap]) -> List[mm.image.MemoryRegionImage]:
        
        image_list: List[mm.image.MemoryRegionImage] = []
        
        mmap_name = next(iter(memory_map_metadata))
        for region_name, region in memory_map_metadata.get(mmap_name).memory_regions.items():
            new_mr_image = mm.image.MemoryRegionImage(
                region_name,
                self.name,
                region,
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
    

    def _add_label(self, dest: PIL.Image, xy: mm.image.Point, len: int, text: str, font_size: int) -> PIL.Image.Image:
        label = mm.image.TextLabelImage(self.name, text, font_size)
        dest = label.overlay(dest, xy)
        return dest

    def _create_mmap(self, memregion_list: List[mm.image.MemoryRegionImage], draw_scale: int):
        """Create a dict of region groups, interleaved with void regions. 
        Then draw the regions onto a larger memory map image. """

        redux_subgroup_idx = 0
        from collections import defaultdict
        redux_subgroup = defaultdict(list)

        for memregion in memregion_list:
            # start adding memregions to the current subgroup...
            redux_subgroup[redux_subgroup_idx].append(memregion)
            # until we hit a empty space larger than the threshold setting
            if memregion.freespace_as_int > self.voidthreshold:
                # add a single void region subgroup at a new index...
                redux_subgroup_idx = redux_subgroup_idx + 1
                redux_subgroup[redux_subgroup_idx].append(self.voidregion)
                # then increment again, ready for next memregion subgroup
                redux_subgroup_idx = redux_subgroup_idx + 1


        map_img_redux = PIL.Image.new(
            "RGBA", 
            (self.width, self.height), 
            color=Diagram.model.bgcolour)
        
        next_void_pos = 0
        last_void_pos = 0 
        for group_idx in range(0, len(redux_subgroup)):

            region: mm.image.MemoryRegionImage
            for region_idx, region in enumerate(redux_subgroup[group_idx]):
                

                if isinstance(region, mm.image.MemoryRegionImage):
                    # adjusted values for drawing ypos - labels should use the original values
                    region_origin_scaled  = region.origin_as_int // draw_scale

                    region._draw()

                    # add memory region after ypos of last voidregion - if any
                    map_img_redux = region.overlay(
                        dest=map_img_redux, 
                        xy=mm.image.Point(0, last_void_pos if last_void_pos else region_origin_scaled), 
                        alpha=int(Diagram.model.region_alpha))
                    
                    # add origin address text
                    map_img_redux = self._add_label(
                        dest=map_img_redux, 
                        xy=mm.image.Point(region.img.width + 5, (last_void_pos if last_void_pos else region_origin_scaled) - 2 ) , 
                        len=1, 
                        text=region.origin_as_hex + " (" + str(region.origin_as_int) + ")", 
                        font_size=region.metadata.address_text_size)
                    
                    # ready the ypos for drawing a void region - if any - after this memregion
                    next_void_pos = (last_void_pos if last_void_pos else region_origin_scaled) + (region.img.height) + 10

                if isinstance(region, mm.image.VoidRegionImage):
                    # add void region
                    map_img_redux.paste(region.img, (0, next_void_pos))
                    # reset the ypos for the next memregion
                    last_void_pos = next_void_pos + region.img.height + 10
                

        # TODO add for region if top most graphic block
        if group_idx == len(redux_subgroup) - 1 and region_idx == len(redux_subgroup[group_idx]) - 1:

            if isinstance(region, mm.image.MemoryRegionImage):
                map_img_redux = self._add_label(
                    dest=map_img_redux, 
                    xy=mm.image.Point(region.img.width + 5, next_void_pos - 20), 
                    len=1, 
                    text=hex(region.origin_as_int + region.size_as_int) + " (" + str(region.origin_as_int + region.size_as_int) + ")", 
                    font_size=10)
                                                
        map_img_redux = self.trim_whitespace(map_img_redux)

        # flip back up the right way
        self.final_map_img_redux = map_img_redux.transpose(PIL.Image.FLIP_TOP_BOTTOM)           
        

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

        # Create the individual memory map diagrams (full and reduced)
        for mmap_name, mmap in Diagram.model.memory_maps.items():
            self.mmd_list.append(MemoryMapDiagram({mmap_name: mmap}))
            pass

        # composite the memory map diagrams into single diagram
        self.draw_diagram_img_redux()

        self._create_table_image(self.mmd_list)
        self._create_markdown(self.mmd_list)        

    def draw_diagram_img_redux(self):
        """add each memory map to the complete diagram image"""
        # self.mmd_list.sort(key=lambda x: x.final_map_img_redux.height, reverse=True)

        max_diagram_height = max(self.mmd_list, key=lambda mmd: mmd.final_map_img_redux.height).final_map_img_redux.height
        max_name_lbl_height = max(self.mmd_list, key=lambda mmd: mmd.name_lbl.img.height).name_lbl.img.height
        
        final_diagram_img = PIL.Image.new(
            "RGBA", 
            (Diagram.model.width, max_diagram_height + max_name_lbl_height + 10), 
            color=Diagram.model.bgcolour)       
        
        # add region and labels first
        for mmd_idx, mmd in enumerate(self.mmd_list):
            
            # add the mem map diagram image
            final_diagram_img.paste(
                mmd.final_map_img_redux.transpose(PIL.Image.FLIP_TOP_BOTTOM), 
                ( (mmd_idx * mmd.width), 0))
            
            # add the mem map name label at this stage so all titles line up at the "top"
            final_diagram_img = mmd.name_lbl.overlay(
                final_diagram_img,
                mm.image.Point( (mmd_idx * mmd.width), final_diagram_img.height - max_name_lbl_height),
                alpha=255)    

        # overlay links on top of everything else
        for source_mmd_idx, mmd in enumerate(self.mmd_list):    
            for region_image in mmd.image_list:
                source_region_mid_pos_x = region_image.abs_mid_pos.x
                source_region_mid_pos_y = region_image.abs_mid_pos.y
                for link in region_image.metadata.links:
                    mmd_parent_name = link[0]
                    region_child_name = link[1]
                    # search for the matching parent/child memmap/memregion
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

                                               
                                    arrow = mm.image.ArrowBlock(
                                        src=mm.image.Point(
                                            (source_mmd_idx * mmd.width) + source_region_mid_pos_x + source_justify,
                                            source_region_mid_pos_y
                                        ),
                                        dst=mm.image.Point(
                                            (target_mmd_idx * mmd.width) + target_region.abs_mid_pos.x + target_justify, 
                                            target_region.abs_mid_pos.y
                                        ),
                                        head_width=25,
                                        tail_len=75,
                                        tail_width=20,
                                        fill=Diagram.model.link_fill_colour,
                                        line=Diagram.model.link_line_colour
                                    )
                                    final_diagram_img = arrow.overlay(final_diagram_img, mm.image.Point(arrow.pos.x, arrow.pos.y), Diagram.model.link_alpha)
     

        # finalise diagram                                                 
        final_diagram_img = final_diagram_img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_file_path = pathlib.Path(Diagram.pargs.out).stem + "_redux.png"
        final_diagram_img.save(pathlib.Path(Diagram.pargs.out).parent / img_file_path)

    def _create_table_image(self, mmd_list: List[MemoryMapDiagram]):
        """Create a png image of the summary table"""

        table_data = []
        for region_map_list in mmd_list:
            for memregion in (region_map_list.image_list):
                table_data.append(memregion)

        # sort by origin value, then expand into list of lists
        table_data.sort(key=lambda x: x.origin_as_int, reverse=True)
        table_data = [d.get_data_as_list() for d in table_data]

        table_img = mm.image.Table().get_table_img(
            table=table_data,
            header=["Map", "Region", "Origin", "Size", "Free Space", "Collisions", "links", "Drawing Scale"],
            font=PIL.ImageFont.load_default(15),
            stock=True,
            colors={"red": "green", "green": "red"},
        )

        tableimg_file_path = pathlib.Path(Diagram.pargs.out).stem + "_table.png"
        table_img.save(pathlib.Path(Diagram.pargs.out).parent / tableimg_file_path)

    def _create_markdown(self,  mmd_list: List[MemoryMapDiagram]):
        """Create markdown doc containing the diagram image """
        """and text-base summary table"""
        table_list: List[mm.image.MemoryRegionImage] = []
        for region_map_list in mmd_list:
            for memregion in (region_map_list.image_list): 
                table_list.append(memregion)           

        # sort by ascending origin value starting from the table bottom
        table_list.sort(key=lambda x: x.origin_as_int, reverse=True)

        with open(Diagram.pargs.out, "w") as f:
            f.write(f"""![memory map diagram]({pathlib.Path(Diagram.pargs.out).stem}_redux.png)\n""")
            f.write("|map|region|origin|size|free Space|collisions|links|draw scale|\n")
            f.write("|:-|:-|:-|:-|:-|:-|:-|:-|\n")
            # use __str__ from mm.image.MemoryRegionImage to print tabulated row
            for mr in table_list:
                f.write(f"{mr}\n")

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

        Diagram.pargs = parser.parse_args()

    @classmethod
    def _validate_pargs(cls):
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
    
    @classmethod
    def _create_model(cls) -> mm.metamodel.Diagram:
        
        if Diagram.pargs.file:
            with pathlib.Path(Diagram.pargs.file).resolve().open("r") as fp:
                inputdict = json.load(fp)
        else:
            mmname = Diagram.pargs.name if Diagram.pargs.name else "Untitled"
            # command line parameters only support one memory map per diagram
            inputdict = {
                "$schema": "../../mm/schema.json",
                "name": "Diagram",
                "height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
                "width": 400 * Diagram.pargs.scale,
                "memory_maps": { 
                    mmname : { 
                        "height": int(Diagram.pargs.limit,16) * Diagram.pargs.scale,
                        "width": 400 * Diagram.pargs.scale,
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
 
