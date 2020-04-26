import pytest

from lissero.Blast import Blast

run_blast = Blast()


def test_blast_version():
    run_blast.version()
    assert ('2', '6', '0') == run_blast.version_no
