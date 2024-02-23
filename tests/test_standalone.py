import subprocess

# sometimes pytest has too much free access to the SUT and doesn't capture issues 
# that might occur with command line invocation

def test_standalone():
    res = subprocess.run(
        ". ./venv/bin/activate && python3 -m mm.diagram -f doc/example/input.json",
        capture_output=True,
        shell=True
    )
    assert res.returncode == 0


