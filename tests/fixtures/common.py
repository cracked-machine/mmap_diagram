import pathlib
import pytest

examples_md_path = pathlib.Path("examples.md")

def init_examples_md_file():
    examples_md_path.unlink(missing_ok=True)
    with open(examples_md_path, 'w', encoding='utf-8') as fp:
        fp.write("||\n")
        fp.write("|-|\n")  

def append_to_examples_md_file(file_path: str, test_desc: str):
    if "docs/example" in file_path:
        with open(examples_md_path, 'a', encoding='utf-8') as mdfp:

            markdown_comment = str(test_desc).replace("\n","")
            markdown_comment = markdown_comment.replace("-","<br>-")

            mdfp.write( f"| <H3>{ file_path } |\n")
            mdfp.write( f"| {markdown_comment} |\n")
            mdfp.write( f"| [![]( { file_path }_diagram.png )]({ file_path }_diagram.png) |\n")    
            mdfp.write( f"| [![]( { file_path }_table.png )]({ file_path }_table.png) |\n")    
            mdfp.write( f"| [{ file_path }.json]({ file_path }.json)<pre>" )

            with open(f"{ file_path }.json", "r", encoding="utf-8") as jsonfp:
                mdfp.write( jsonfp.read().replace("\n", "<BR>") )

            mdfp.write( f"</pre> |\n" )

@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    init_examples_md_file()
    
@pytest.fixture()
def test_setup(request):

    # Setup some file paths. Make sure they are deleted before starting the unit test
    report = pathlib.Path(f"{request.param['file_path']}.md")
    report.unlink(missing_ok=True)

    diagram_image = pathlib.Path(f"{request.param['file_path']}_diagram.png")
    diagram_image.unlink(missing_ok=True)

    table_image = pathlib.Path(f"{request.param['file_path']}_table.png")
    table_image.unlink(missing_ok=True)

    json_file = pathlib.Path(f"{request.param['file_path']}.json")
    table_image.unlink(missing_ok=True)

    # send the path variables back to the calling unit test function
    yield {"report": report, "diagram_image": diagram_image, "table_image": table_image, "json_file": json_file}

    # finally add the generated files for this test to the examples.md file
    append_to_examples_md_file(request.param['file_path'], request.param['test_desc'])

