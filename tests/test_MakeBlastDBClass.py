import pytest

from lissero.scripts.Blast import MakeBlastDB

run_mkdb = MakeBlastDB()


def test_makeblastdb_version(blast_version):
    run_mkdb.version()
    expected = tuple(blast_version.split("."))
    assert expected == run_mkdb.version_no
