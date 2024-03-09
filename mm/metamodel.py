
import pydantic
import pathlib
import json
from typing import Tuple, Literal, Union
from typing_extensions import Annotated
import logging
import enum
import math

ColourType = Union[str | Tuple[int, int, int]]

class ConfigParent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        revalidate_instances="always",
        validate_default=True,
        validate_return=True,
        use_enum_values=True
    )

class IndentScheme(str, enum.Enum):
    linear = 'linear'
    alternate = 'alternate'
    inline = 'inline'

# data model
class MemoryRegion(ConfigParent):

    origin: Annotated[
        int | str,
        pydantic.Field(..., description="Origin address of the MemoryMap. In hex format string."),
    ]
    size: Annotated[
        int | str,
        pydantic.Field(..., description="Size (in bytes) of the MemoryMap. In hex format string."),
    ]
    links: list[tuple[str,str]] = pydantic.Field(
        [],
        description="""Links to other memory regions. E.g. """
        """\n["""
        """\n\n{'ParentMemoryMap1': 'ChildMemoryRegion1'}"""
        """\n\n..."""
        """\n\n{'ParentMemoryMapN': 'ChildMemoryRegionN'}"""
        """\n]""")
    
    # TODO Make this underscore so it doesn't get serialised into the json schema
    freespace: Annotated[
        int,
        pydantic.Field("", description="Internal Use")
    ]

    # TODO Make this underscore so it doesn't get serialised into the json schema
    collisions: Annotated[
        dict,
        pydantic.Field({}, Description="Internal Use")
    ]
    text_size: Annotated[
        int, 
        pydantic.Field(0, description="The text size for this region", exclude=True)
    ]
    address_text_size: Annotated[
        int, 
        pydantic.Field(0, description="The text size for this region", exclude=True)
    ]

    @pydantic.field_validator("freespace", mode="before")
    @classmethod
    def convert_str_to_int(cls, v: str):
        if isinstance(v, str):
            if v == "":
                return 0
            else:
                return int(v, 16)
        else:
            return v

    @pydantic.field_validator("origin", "size", mode="before")
    @classmethod
    def check_empty_str(cls, v: any):
        assert v, "Empty value found!"
        if isinstance(v, int):
            v = hex(v)
        assert v[:2] == "0x"
        return int(v, 16)

class MemoryMap(ConfigParent):

    memory_regions: Annotated[
        dict[str, MemoryRegion],
        pydantic.Field(description="Memory map containing memory regions.")
    ]
    height: Annotated[
        int,
        pydantic.Field(
            0, 
            description="""Internal Use. 
            This will be automically adjusted depending on the diagram size and number of memory maps.""", 
            exclude=True)
    ]
    width: Annotated[
        int,
        pydantic.Field(
            0, 
            description="""Internal Use. 
            This will be automically adjusted depending on the diagram size and number of memory maps.""", 
            exclude=True)
    ]
    draw_scale:Annotated [
        int,
        pydantic.Field(
            1, 
            description="Drawing scale denominator. Internal use only.", 
            exclude=True)
    ]
    max_address: Annotated[
        int,
        pydantic.Field(
            0,
            description="""Max address for the map. Use hex. 
            If not defined, max_address will be determined by the region data."""
        )
    ]
    max_address_calculated: Annotated[
        bool,
        pydantic.Field(
            False,
            description="Internal Use",
            exclude=True
        )
    ]

    @pydantic.field_validator("max_address", mode="before")
    @classmethod
    def convert_str_to_int(cls, v: str):
        if isinstance(v, str):
            if v == "":
                return 0
            else:
                return int(v, 16)
        else:
            return v

class Diagram(ConfigParent):

    address_text_size: Annotated[
        int, 
        pydantic.Field(12, description="The text size for this region", exclude=True)
    ]
    bgcolour: Annotated[
        ColourType,
        pydantic.Field("white", description="The background colour used for the diagram")
    ] 
    link_alpha: Annotated[
        int,
        pydantic.Field(96, description="Transparency value for all link arrow images.", gt=-1, lt=256)
    ]
    link_fill_colour: Annotated[
        ColourType,
        pydantic.Field("red", description="Fill colour for the link arrows")
    ]
    link_line_colour: Annotated[
        ColourType,
        pydantic.Field("red", description="Line colour for the link arrows")
    ]
    link_head_width: Annotated[
        int, 
        pydantic.Field(
            25,
            description="Arrow head width (pixels) of the region link graphic.",
            exclude=True
        )
    ]
    link_tail_len: Annotated[
        int, 
        pydantic.Field(
            75,
            description="Arrow tail length (percentage, relative to arrow head) of the region link graphic.",
            exclude=True
        )
    ]
    link_tail_width: Annotated[
        int, 
        pydantic.Field(
            20,
            description="Arrow tail width (percentage, relative to arrow head) of the region link graphic.",
            exclude=True
        )
    ]
    legend_width: Annotated[
        int,
        pydantic.Field(30, description="The percentage width of the diagram legend")
    ]
    memory_maps: Annotated[
        dict[str, MemoryMap],
        pydantic.Field(..., description="MemoryMap sub-diagram contents.")
    ]
    name: Annotated[
        str, 
        pydantic.Field(..., description="The name of the diagram.")
    ]
    height: Annotated[
        int,
        pydantic.Field(..., 
                       description="""The height of the diagram in pixels. 
                       If a region size exceeds this height value, 
                       then the region size will be scaled to fit within the diagram height.""")
    ]
    indent_scheme: Annotated[
        IndentScheme,
        pydantic.Field(
            IndentScheme.alternate, 
            description="Drawing indent for Memory Regions. Enabled for colliding regions only.")
    ]
    region_alpha: Annotated[
        int,
        pydantic.Field(192, description="Transparency value for all region block images.", gt=-1, lt=256)
    ]
    threshold: Annotated[
        int | str,
        pydantic.Field(
            hex(200),
            description="The threshold for skipping void sections. Please use hex."            
        )
    ]
    title_fill_colour: Annotated[
        ColourType,
        pydantic.Field((224,224,224), description="Fill colour for the memory map title blocks")
    ]
    text_size: Annotated[
        int, 
        pydantic.Field(
            14, 
            description="""The text size used for entire diagram. 
            Region text size can be overridden""", 
            exclude=True)
    ]
    title_line_colour: Annotated[
        ColourType,
        pydantic.Field((32,32,32), description="Line colour for the memory map title blocks")
    ]
    void_fill_colour: Annotated[
        ColourType,
        pydantic.Field("white", description="Fill colour for the void region blocks")
    ]
    void_line_colour: Annotated[
        ColourType,
        pydantic.Field((192,192,192), description="Line colour for the void region blocks")
    ]
    width: Annotated[
        int,
        pydantic.Field(..., description="The width of the diagram in pixels.")
    ]

    @pydantic.field_validator("threshold", mode="before")
    @classmethod
    def convert_str_to_int(cls, v: str):
        if isinstance(v, str):
            if v == "":
                return 0
            else:
                return int(v, 16)
        else:
            return v

    @pydantic.field_validator("name")
    @classmethod
    def check_empty_str(cls, v: str):
        assert v, "Empty string found!"
        return v

    @pydantic.field_validator("memory_maps")
    @classmethod
    def check_dangling_region_links(cls, v: dict[str, MemoryMap]):
        found_memory_regions = []
        found_region_links = []
        

        # get all region_link properties from the data
        for mmap_name, mmap in v.items():
            for region in mmap.memory_regions.items():
                found_memory_regions.append(region)
                
                for regionlink in region[1].links:
                    found_region_links.append(
                        {
                            "source_map_name": mmap_name, 
                            "source_region_name": region[0], 
                            "target_link": regionlink, 
                            "target_region_size": region[1].size
                        }
                    )
                    

        # check found links ref existing memmaps and memregions
        for regionlink in found_region_links:

            region_link_parent_memmap = regionlink['target_link'][0]
            assert any(
                (mm_name == region_link_parent_memmap) for mm_name in v.keys()),\
                f"Parent MemoryMap '{region_link_parent_memmap}' in {regionlink['target_link']} is a dangling reference!"
            
            region_link_child_memregion = regionlink['target_link'][1]     
            assert any((mr[0] == region_link_child_memregion for mr in found_memory_regions)),\
                f"Child MemoryRegion '{region_link_child_memregion}' in {regionlink['target_link']} is a dangling reference!"

            # also check the from/to memoryregions are the same size
            for mr in found_memory_regions:
                if mr[0] == region_link_child_memregion:
                    assert mr[1].size == regionlink['target_region_size'],\
                    f"Size mismatch from link {regionlink['source_map_name']}.{regionlink['source_region_name']} to {region_link_parent_memmap}.{region_link_child_memregion}"

        return v

    @pydantic.model_validator(mode="after")
    def resize_memory_maps_to_fit_diagram_width(self):
        """ Resize the multiple memory maps to fit within the diagram"""
        # assume all memory maps should always be same height as overall diagram
        for memory_map in self.memory_maps.values():
            memory_map.height = self.height
        
        new_memory_map_width = self.width // len(self.memory_maps) 
        new_memory_map_width - 10 # allow for some extra space
        for memory_map in self.memory_maps.values():
            memory_map.width = new_memory_map_width

        return self

    @pydantic.model_validator(mode="after")
    def set_region_text_size(self):
        """If user did not set memregion text size (default is 0) then use the diagram-wide setting"""
        memmap: MemoryMap
        for memmap in self.memory_maps.values():
            memregion: MemoryRegion
            for memregion in memmap.memory_regions.values():
                if  memregion.text_size == 0:
                    memregion.text_size = self.text_size
                if  memregion.address_text_size == 0:
                    memregion.address_text_size = self.address_text_size

        return self
    
    @pydantic.model_validator(mode="after")
    def calc_nearest_region(self):
        """Find the nearest neighbour region and if they have collided"""
        logging.debug("")
        logging.debug("Calculating distances")
        logging.debug("---------------------")
        # process each memory map independently
        for mname, memory_map in self.memory_maps.items():
            
            # determine if drawing scale is needed by finding if the largest memoryregion exceeds the diagram height
            # NOTE: for simplicities sake we calculate distances/freespace using the original 1:1 scale,
            # we only scale values afterwards when they are recorded for stats purposes.
            largest_region = 0
            for region in memory_map.memory_regions.values():
                if region.origin + region.size > largest_region:
                    largest_region = region.origin + region.size

            # # in case there is a voidregion at the top of the diagram
            # largest_region = largest_region + (self.text_size + 10)
            # memory_map.max_address = memory_map.max_address + (self.text_size + 10)

            # max address should be at least equal to the region data or greater
            if not memory_map.max_address or memory_map.max_address < largest_region:
                memory_map.max_address_calculated = True
                memory_map.max_address = largest_region
            
            # calc the drawing scale from whichever is the greatest: max address or the region data
            memory_map.draw_scale = math.ceil(
                max(largest_region, memory_map.max_address) / memory_map.height)


            neighbour_region_list = memory_map.memory_regions.items()
            
            for memory_region_name, memory_region in memory_map.memory_regions.items(): 
                non_collision_distances = {}

                logging.debug(f"{memory_region_name} region:")
                this_region_end = 0

                # examine all other region distances relative to this region position
                other_region: Tuple[str, MemoryRegion]
                for other_region in neighbour_region_list:

                    # calc the end address of this and the next other region
                    other_region_name = other_region[0]
                    other_region_origin = other_region[1].origin
                    other_region_size = other_region[1].size

                    this_region_end: int = memory_region.origin + memory_region.size
                    other_region_end: int = other_region_origin + other_region_size                  

                    # skip calculating distance from yourself.
                    if memory_region_name == other_region_name:
                        continue

                    # skip if 'this' region origin is ahead of the probed region end address
                    if memory_region.origin >= other_region_end:
                        continue

                    distance_to_other_region: int = other_region_origin - this_region_end
                    logging.debug(f"\t{hex(distance_to_other_region)} bytes to {other_region_name}")

                    # collision detected
                    if distance_to_other_region < 0:
                        # was the region that collided into us at a lower or higher origin address
                        if other_region_origin < memory_region.origin:
                            # lower so use our origin address as the collion point
                            memory_region.collisions[other_region_name] = memory_region.origin
                        else:
                            # higher so use their origin address as the collision point
                            memory_region.collisions[other_region_name] = other_region_origin

                        # no distance left
                        if memory_region.origin < other_region_origin:
                            memory_region.freespace = distance_to_other_region

                    else:
                        # record the distance for later 
                        non_collision_distances[other_region_name] = distance_to_other_region
                        # set a first value while we have it (in case there are no future collisions)
                        if not memory_region.freespace and not memory_region.collisions:
                            memory_region.freespace = distance_to_other_region
                        # if remain not already set to no distance left then set the positive remain distance
                        elif not memory_region.freespace:
                            memory_region.freespace = distance_to_other_region

                logging.debug(f"\tCollisions - {memory_region.collisions}")

                # after probing each region we must now pick the lowest distance
                if not memory_region.collisions:
                    if non_collision_distances:
                        # there are other regions ahead of this one, so find the nearest one
                        lowest = min(non_collision_distances, key=non_collision_distances.get)
                        memory_region.freespace = non_collision_distances[lowest]
                    else:
                        # there are no regions ahead of this one
                        memory_region.freespace = memory_map.max_address - (this_region_end)
                elif memory_region.collisions and not memory_region.freespace:
                    memory_region.freespace = memory_map.max_address - (this_region_end)

                # the user-defined max_address field has created an excessive amount of empty space, clamp it to the region data usage instead
                if memory_region.freespace > self.height:
                    logging.warning(f"'{mname}' Region freespace exceeds diagram height: {memory_region.freespace} > {self.height}.")
                    logging.warning(f"You have set your 'max_address' to {memory_map.max_address} but none of your regions are using the excessive empty space this has created.")
                    logging.warning(f"Drawing ratio (1:{str(memory_map.draw_scale)}) will be readjusted.")
                    memory_map.draw_scale = math.ceil((largest_region) / memory_map.height)
                    # if the 'draw_scale' means we end up close to the diagram top edge 
                    # then add some space for a voidregion (if any)
                    if math.ceil(largest_region / memory_map.draw_scale) >= memory_map.height:
                        memory_map.draw_scale = math.ceil((largest_region + (800000)) / memory_map.height)
                    
                    logging.warning(f"Recalculating drawing ratio: (1:{str(memory_map.draw_scale)})")

        return self

    
# helper functions
def generate_schema(path: pathlib.Path):
    myschema = Diagram.model_json_schema()

    with path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))

if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



