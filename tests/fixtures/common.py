import pathlib
import pytest

markdown = pathlib.Path("examples.md")

@pytest.fixture(scope="session", autouse=True)
def markdown_setup(request):
    markdown.unlink(missing_ok=True)
    with open(markdown, 'w', encoding='utf-8') as fp:
        fp.write("||\n")
        fp.write("|-|\n")  
    
@pytest.fixture()
def file_setup(request):

    report = pathlib.Path(f"{request.param['file_path']}.md")
    report.unlink(missing_ok=True)

    diagram_image = pathlib.Path(f"{request.param['file_path']}_diagram.png")
    diagram_image.unlink(missing_ok=True)

    table_image = pathlib.Path(f"{request.param['file_path']}_table.png")
    table_image.unlink(missing_ok=True)

    json_file = pathlib.Path(f"{request.param['file_path']}.json")
    table_image.unlink(missing_ok=True)

    yield {"report": report, "diagram_image": diagram_image, "table_image": table_image, "json_file": json_file}

    if "docs/example" in request.param['file_path']:
        with open(markdown, 'a', encoding='utf-8') as mdfp:

            markdown_comment = str(request.param['test_desc']).replace("\n","")
            markdown_comment = markdown_comment.replace("-","<br>-")
            file_path = request.param['file_path']
            mdfp.write( f"| <H3>{file_path} |\n")
            mdfp.write( f"| {markdown_comment} |\n")
            mdfp.write( f"| [![]( {file_path}_diagram.png )]({file_path}_diagram.png) |\n")    
            mdfp.write( f"| [![]( {file_path}_table.png )]({file_path}_table.png) |\n")    
            mdfp.write( f"| [{file_path}.json]({file_path}.json)<pre>" )

            with open(f"{file_path}.json", "r", encoding="utf-8") as jsonfp:
                mdfp.write( jsonfp.read().replace("\n", "<BR>") )

            mdfp.write( f"</pre> |\n" )

