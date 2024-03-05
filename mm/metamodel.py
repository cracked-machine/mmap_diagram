
import pydantic
import pathlib
import json
from typing import Tuple, Literal
from typing_extensions import Annotated
import logging
import enum

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

    memory_region_origin: Annotated[
        int,
        pydantic.Field(..., description="Origin address of the MemoryMap. In hex format string."),
    ]
    memory_region_size: Annotated[
        int,
        pydantic.Field(..., description="Size (in bytes) of the MemoryMap. In hex format string."),
    ]
    memory_region_links: list[tuple[str,str]] = pydantic.Field(
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

    @pydantic.field_validator("memory_region_origin", "memory_region_size", mode="before")
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
    map_height: Annotated[
        int,
        pydantic.Field(0, description="Internal Use. This will be automically adjusted depending on the diagram size and number of memory maps.")
    ]
    map_width: Annotated[
        int,
        pydantic.Field(0, description="Internal Use. This will be automically adjusted depending on the diagram size and number of memory maps.")
    ]

class Diagram(ConfigParent):

    # diagram_name: str = pydantic.Field(description="The name of the diagram.")
    diagram_name: Annotated[
        str, 
        pydantic.Field(..., description="The name of the diagram.")
    ]
    diagram_height: Annotated[
        int,
        pydantic.Field(..., description="The height of the diagram.")
    ]
    diagram_width: Annotated[
        int,
        pydantic.Field(..., description="The width of the diagram.")
    ]
    diagram_legend_width: Annotated[
        int,
        pydantic.Field(30, description="The percentage width of the diagram legend")
    ]
    diagram_bgcolour: Annotated[
        str,
        pydantic.Field("white", description="The background colour used for the diagram")
    ] 
    void_fill_colour: Annotated[
        str,
        pydantic.Field("lightgrey", description="Fill colour for the void region blocks")
    ]
    void_line_colour: Annotated[
        str,
        pydantic.Field("grey", description="Line colour for the void region blocks")
    ]
    title_fill_colour: Annotated[
        str,
        pydantic.Field("blanchedalmond", description="Fill colour for the memory region title blocks")
    ]
    title_line_colour: Annotated[
        str,
        pydantic.Field("grey", description="Line colour for the emory region title blocks")
    ]
    memory_maps: Annotated[
        dict[str, MemoryMap],
        pydantic.Field(..., description="The diagram frame. Can contain many memory maps.")
    ]
    indent_scheme: Annotated[
        IndentScheme,
        pydantic.Field(IndentScheme.alternate, description="Drawing indent for Memory Regions")
    ]

    @pydantic.field_validator("diagram_name")
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
                
                for regionlink in region[1].memory_region_links:
                    found_region_links.append(
                        {
                            "source_map_name": mmap_name, 
                            "source_region_name": region[0], 
                            "target_link": regionlink, 
                            "target_region_size": region[1].memory_region_size
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
                    assert mr[1].memory_region_size == regionlink['target_region_size'],\
                    f"Size mismatch from link {regionlink['source_map_name']}.{regionlink['source_region_name']} to {region_link_parent_memmap}.{region_link_child_memregion}"


            # assert any((mr[1].memory_region_size == regionlink['target_region_size'] for mr in found_memory_regions)),\
            #     f"Size mismatch between {region_link_parent_memmap}.{mr.name} and {region_link_parent_memmap}.{ regionlink['target_region_size']}"

        return v

    @pydantic.model_validator(mode="after")
    def resize_memory_maps_to_fit_diagram_width(self):
        """ Resize the multiple memory maps to fit within the diagram"""
        # assume all memory maps should always be same height as overall diagram
        for memory_map in self.memory_maps.values():
            memory_map.map_height = self.diagram_height
        
        # command line input (only one memory map possible)
        if len(self.memory_maps) == 1:
            pass
        else:
            new_memory_map_width = self.diagram_width // len(self.memory_maps) 
            new_memory_map_width - 10 # allow for some extra space
            for memory_map in self.memory_maps.values():
                memory_map.map_width = new_memory_map_width

        return self

    @pydantic.model_validator(mode="after")
    def calc_nearest_region(self):
        """Find the nearest neighbour region and if they have collided"""

        # process each memory map independently
        for memory_map in self.memory_maps.values():
            
            neighbour_region_list = memory_map.memory_regions.items()
            
            for memory_region_name, memory_region in memory_map.memory_regions.items(): 
                non_collision_distances = {}

                logging.debug(f"Calculating nearest distances to {memory_region_name} region:")
                this_region_end = 0

                other_region: Tuple[str, MemoryRegion]
                for other_region in neighbour_region_list:
                    # calc the end address of this and inspected region
                    other_region_name = other_region[0]
                    other_region_origin = other_region[1].memory_region_origin
                    other_region_size = other_region[1].memory_region_size

                    this_region_end: int = memory_region.memory_region_origin + memory_region.memory_region_size
                    other_region_end: int = other_region_origin + other_region_size

                    # skip calculating distance from yourself.
                    if memory_region_name == other_region_name:
                        continue

                    # skip if 'this' region origin is ahead of the probed region end address
                    if memory_region.memory_region_origin >= other_region_end:
                        continue

                    distance_to_other_region: int = other_region_origin - this_region_end
                    logging.debug(f"\t{hex(distance_to_other_region)} bytes to {other_region_name}")

                    # collision detected
                    if distance_to_other_region < 0:
                        # was the region that collided into us at a lower or higher origin address
                        if other_region_origin < memory_region.memory_region_origin:
                            # lower so use our origin address as the collion point
                            memory_region.collisions[other_region_name] = memory_region.memory_region_origin
                        else:
                            # higher so use their origin address as the collision point
                            memory_region.collisions[other_region_name] = other_region_origin

                        if memory_region.memory_region_origin < other_region_origin:
                            # no distance left
                            memory_region.freespace = distance_to_other_region
                            pass

                    else:
                        # record the distance for later
                        non_collision_distances[other_region_name] = distance_to_other_region
                        # set a first value while we have it (in case there are no future collisions)
                        if not memory_region.freespace and not memory_region.collisions:
                            memory_region.freespace = distance_to_other_region
                        # # if remain not already set to no distance left then set the positive remain distance
                        elif not memory_region.freespace:
                            memory_region.freespace = distance_to_other_region

                logging.debug(f"Non-collision distances - {non_collision_distances}")

                # after probing each region we must now pick the lowest distance ()
                if not memory_region.collisions:
                    if non_collision_distances:
                        lowest = min(non_collision_distances, key=non_collision_distances.get)
                        memory_region.freespace = non_collision_distances[lowest]
                    else:
                        memory_region.freespace = memory_map.map_height - this_region_end
                elif memory_region.collisions and not memory_region.freespace:
                    memory_region.freespace = memory_map.map_height - this_region_end

    
# helper functions
def generate_schema(path: pathlib.Path):
    myschema = Diagram.model_json_schema()

    with path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))

if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



