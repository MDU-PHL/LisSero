"""
Configure testes
"""

# add a parameter to the command line to specify the version of blast
# when testing the blast version
def pytest_addoption(parser):
    parser.addoption("--blast-version", action="store", default="2.9.0", help="Specify the BLAST version")

def pytest_generate_tests(metafunc):
    if "blast_version" in metafunc.fixturenames:
        metafunc.parametrize("blast_version", [metafunc.config.getoption("blast_version")])
