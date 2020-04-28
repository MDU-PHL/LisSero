import pytest

from lissero.scripts.Blast import MakeBlastDB

run_mkdb = MakeBlastDB()


def test_makeblastdb_version():
    run_mkdb.version()
    assert ('2', '10', '0') == run_mkdb.version_no
