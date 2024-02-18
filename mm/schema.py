
import pydantic
import pathlib
import json
from typing_extensions import Annotated


class ConfigParent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        revalidate_instances="always",
        validate_default=True,
        validate_return=True
    )


# data model
class MemoryRegion(ConfigParent):

    memory_region_origin: Annotated[
        str,
        pydantic.Field(..., description="Origin address of the MemoryMap. In hex format string."),
    ]
    memory_region_size: Annotated[
        str,
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

    @pydantic.model_validator(mode="after")
    def check_empty_str(self):
        
        assert self.memory_region_origin, "Empty string found!"
        assert self.memory_region_origin[:2] == "0x"

        assert self.memory_region_size, "Empty string found!"
        assert self.memory_region_size[:2] == "0x"

        return self


class MemoryMap(ConfigParent):

    memory_regions: Annotated[
        dict[str, MemoryRegion],
        pydantic.Field(description="Memory map containing memory regions.")
    ]


class Diagram(ConfigParent):

    # diagram_name: str = pydantic.Field(description="The name of the diagram.")
    diagram_name: Annotated[
        str, 
        pydantic.Field(..., description="The name of the diagram.")
    ]
    memory_maps: Annotated[
        dict[str, MemoryMap],
        pydantic.Field(..., description="The diagram frame. Can contain many memory maps.")
    ]

    @pydantic.model_validator(mode="after")
    def check_empty_str(self):
        
        assert self.diagram_name, "Empty string found!"

        return self

    @pydantic.model_validator(mode="after")
    def check_dangling_region_links(self):
        found_memory_regions = []
        found_region_links = []
        v = self.memory_maps

        # get all region_link properties from the data
        for mmap in v.values():
            for region in mmap.memory_regions.items():
                found_memory_regions.append(region)
                
                for regionlink in region[1].memory_region_links:
                    found_region_links.append({"link": regionlink, "region_size": region[1].memory_region_size})
                    

        # check found links ref existing memmaps and memregions
        for regionlink in found_region_links:

            region_link_parent_memmap = regionlink['link'][0]
            assert any(
                (mm_name == region_link_parent_memmap) for mm_name in v.keys()),\
                f"Parent MemoryMap '{region_link_parent_memmap}' in {regionlink['link']} is a dangling reference!"
            
            # also check the from/to memoryregions are the same size
            region_link_child_memregion = regionlink['link'][1]     
            assert any(
                (mr[0] == region_link_child_memregion and
                mr[1].memory_region_size == regionlink['region_size']) 
                for mr in found_memory_regions),\
                f"Child MemoryRegion '{region_link_child_memregion}' in {regionlink['link']} is a dangling reference!"

        return self
    
# helper functions
def generate_schema(path: pathlib.Path):
    myschema = Diagram.model_json_schema()

    with path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))

if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



