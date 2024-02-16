from pydantic import BaseModel, Field, ConfigDict
import pathlib
import json
from typing import Optional, Dict
    
class MemoryRegion(BaseModel):
    name: str = Field(
        "<RegionName>",
        description="Name of the MemoryMap.",

    )
    origin: str = Field("0x", description="Origin address of the MemoryMap. In hex format string.")
    size: Optional[str] = Field("0x", description="Size (in bytes) of the MemoryMap. In hex format string.")
    regionlinks: list[Dict[str,str]] = Field(
        [
            {"<ParentMapName>" : "<ChildRegionName>"}
        ], 
        description="Link to another memory region. E.g. <MemoryMap:name>.<MemoryRegion:Name>")

class MemoryMap(BaseModel):
    name: str = Field(
        "<MapName>",
        description="Name of the memory map"
        
    )
    MemoryMap: list[MemoryRegion] = Field(
        [
            {
                "name": "<RegionName>",
                "origin": "0x",
                "size": "0x",
                "regionlinks": [
                    {"<ParentMapName>" : "<ChildRegionName>"}
                ]
            }
        ],
        description="Memory map containing memory regions.")

class Diagram(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        revalidate_instances="always",
        validate_default=True
    )
    
    
    Diagram: list[MemoryMap] = Field(
        [
            {
                "name": "Map1",
                "MemoryMap": [
                    {
                        "name": "<RegionName>",
                        "origin": "0x",
                        "size": "0x",
                        "regionlinks": [
                             {"<ParentMapName>" : "<ChildRegionName>"}
                        ]
                    }
                ]
            }
        ], 
        description="The diagram frame. Can contain many memory maps.")


def generate_schema():
    schema_path = pathlib.Path("./mm/schema.json")
    myschema = Diagram.model_json_schema()
    myschema['required'] = ['Diagram']
    myschema['$defs']['MemoryMap']['required'] = ['name', 'MemoryMap']
    myschema['$defs']['MemoryRegion']['required'] = ['name', 'origin', 'size']
    
    with schema_path.open("w") as fp:
        fp.write(json.dumps(myschema, indent=2))


if __name__  == "__main__":
    generate_schema()



