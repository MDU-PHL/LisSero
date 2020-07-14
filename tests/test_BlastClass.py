import pytest

from lissero.scripts.Blast import Blast

run_blast = Blast()


def test_blast_version(blast_version):
    print(f"Testing version {blast_version}")
    run_blast.version()
    expected = tuple(blast_version.split("."))
    assert expected == run_blast.version_no
