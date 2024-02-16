from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import AfterValidator
import pathlib
import json
from typing import Optional, Dict
from typing_extensions import Annotated

# Validators
def check_empty_str(v: str):
    assert v
    return v

def check_hex_str(v:str):
    assert v[:2] == "0x"
    return v

# data model
class MemoryRegion(BaseModel):
    memory_region_name: Annotated[
        str,
        Field(description="Name of the MemoryMap."),
        AfterValidator(check_empty_str)
    ]

    memory_region_origin: Annotated[
        str,
        Field(description="Origin address of the MemoryMap. In hex format string."),
        AfterValidator(check_empty_str),
        AfterValidator(check_hex_str)
    ]
    memory_region_size: Annotated[
        str,
        Field(description="Size (in bytes) of the MemoryMap. In hex format string."),
        AfterValidator(check_empty_str),
        AfterValidator(check_hex_str)
    ]
    memory_region_links: list[Dict[str,str]] = Field(
        [{"<ParentMemoryMap>": "<ChildMemoryRegion>"}],
        description="Link to another memory region. E.g. <MemoryMap:name>.<MemoryRegion:Name>")

class MemoryMap(BaseModel):
    memory_map_name: Annotated[
        str,
        Field(description="Name of the memory map."),
        AfterValidator(check_empty_str)        
    ]
    memory_regions: list[MemoryRegion] = Field(description="Memory map containing memory regions.")

class Diagram(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        revalidate_instances="always",
        validate_default=True,
    )

    # diagram_name: str = Field(description="The name of the diagram.")
    diagram_name: Annotated[
        str, 
        Field(description="The name of the diagram."),
        AfterValidator(check_empty_str)
    ]
    memory_maps: list[MemoryMap] = Field(description="The diagram frame. Can contain many memory maps.")

    
# helper functions
def generate_schema(path: pathlib.Path):
    schema_path = pathlib.Path("./mm/schema.json")
    myschema = Diagram.model_json_schema()

    with schema_path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))


if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



