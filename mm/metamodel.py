
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
        pydantic.Field(0, description="Internal Use. This will be automically adjusted depending on the diagram size and number of memory maps.", exclude=True)
    ]
    width: Annotated[
        int,
        pydantic.Field(0, description="Internal Use. This will be automically adjusted depending on the diagram size and number of memory maps.", exclude=True)
    ]
    draw_scale:Annotated [
        int,
        pydantic.Field(1, description="Drawing scale denominator. Internal use only.", exclude=True)
    ]

class Diagram(ConfigParent):

    # name: str = pydantic.Field(description="The name of the diagram.")
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
    width: Annotated[
        int,
        pydantic.Field(..., description="The width of the diagram in pixels.")
    ]
    legend_width: Annotated[
        int,
        pydantic.Field(30, description="The percentage width of the diagram legend")
    ]
    bgcolour: Annotated[
        ColourType,
        pydantic.Field("white", description="The background colour used for the diagram")
    ] 
    void_fill_colour: Annotated[
        ColourType,
        pydantic.Field("white", description="Fill colour for the void region blocks")
    ]
    void_line_colour: Annotated[
        ColourType,
        pydantic.Field((192,192,192), description="Line colour for the void region blocks")
    ]
    title_fill_colour: Annotated[
        ColourType,
        pydantic.Field((224,224,224), description="Fill colour for the memory map title blocks")
    ]
    title_line_colour: Annotated[
        ColourType,
        pydantic.Field((32,32,32), description="Line colour for the memory map title blocks")
    ]
    memory_maps: Annotated[
        dict[str, MemoryMap],
        pydantic.Field(..., description="MemoryMap sub-diagram contents.")
    ]
    indent_scheme: Annotated[
        IndentScheme,
        pydantic.Field(IndentScheme.alternate, description="Drawing indent for Memory Regions")
    ]
    region_alpha: Annotated[
        int,
        pydantic.Field(192, description="Transparency value for all region block images.", gt=-1, lt=256)
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
    def calc_nearest_region(self):
        """Find the nearest neighbour region and if they have collided"""

        # process each memory map independently
        for memory_map in self.memory_maps.values():
            
            # determine if drawing scale is needed by finding if the largest memoryregion exceeds the diagram height
            # NOTE: for simplicities sake we calculate distances/freespace using the original 1:1 scale,
            # we only scale values afterwards when they are recorded for stats purposes.
            largest_region = 0
            for region in memory_map.memory_regions.values():
                if region.origin + region.size > largest_region:
                    largest_region = region.origin + region.size
            
            memory_map.draw_scale = math.ceil(largest_region / memory_map.height)


            neighbour_region_list = memory_map.memory_regions.items()
            
            for memory_region_name, memory_region in memory_map.memory_regions.items(): 
                non_collision_distances = {}

                logging.debug(f"Calculating nearest distances to {memory_region_name} region:")
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

                logging.debug(f"Non-collision distances - {non_collision_distances}")

                # after probing each region we must now pick the lowest distance
                if not memory_region.collisions:
                    if non_collision_distances:
                        # there are other regions ahead of this one, so find the nearest one
                        lowest = min(non_collision_distances, key=non_collision_distances.get)
                        memory_region.freespace = non_collision_distances[lowest]
                    else:
                        # there are no regions ahead of this one
                        memory_region.freespace = memory_map.height - (this_region_end // memory_map.draw_scale)
                elif memory_region.collisions and not memory_region.freespace:
                    memory_region.freespace = memory_map.height - (this_region_end)


    
# helper functions
def generate_schema(path: pathlib.Path):
    myschema = Diagram.model_json_schema()

    with path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))

if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



