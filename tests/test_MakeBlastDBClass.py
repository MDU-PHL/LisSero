import pytest

from lissero.Blast import MakeBlastDB

run_mkdb = MakeBlastDB()


def test_makeblastdb_version():
    run_mkdb.version()
    assert ('2', '6', '0') == run_mkdb.version_no
