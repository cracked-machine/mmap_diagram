from pydantic import BaseModel, Field, ConfigDict, field_validator
import pathlib
import json
from typing import Optional, Dict
    
class MemoryRegion(BaseModel):
    name: str = Field(description="Name of the MemoryMap.")

    origin: str = Field(description="Origin address of the MemoryMap. In hex format string.")
    size: Optional[str] = Field(description="Size (in bytes) of the MemoryMap. In hex format string.")
    regionlinks: list[Dict[str,str]] = Field(
        description="Link to another memory region. E.g. <MemoryMap:name>.<MemoryRegion:Name>")

class MemoryMap(BaseModel):
    name: str = Field(description="Name of the memory map"
        
    )
    MemoryMap: list[MemoryRegion] = Field(description="Memory map containing memory regions.")

class Diagram(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        revalidate_instances="always",
        validate_default=True,
    )

    Diagram: list[MemoryMap] = Field(description="The diagram frame. Can contain many memory maps.")
    

def generate_schema(path: pathlib.Path):
    schema_path = pathlib.Path("./mm/schema.json")
    myschema = Diagram.model_json_schema()

    with schema_path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))


if __name__  == "__main__":
    generate_schema(pathlib.Path("./mm/schema.json"))



