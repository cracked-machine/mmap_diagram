import unittest
import pytest
import pathlib
import mm.datamodel


@pytest.fixture
def setup():
    schema = pathlib.Path("./mm/schema.json")
    schema.unlink(missing_ok=True)
    return {"schema": schema}

def test_schema_gen(setup):
    mm.datamodel.generate_schema()
    assert setup["schema"].exists()