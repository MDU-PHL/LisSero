import pytest
import os
from lissero.Serotype import SerotypeDB
from lissero.Blast import Blast
from lissero.Sample import Sample

BLAST_OUTFMT = '6 qaccver saccver length slen pident'

test_folder = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(os.path.dirname(test_folder), 'db')
sero_infile = os.path.join(db_folder, 'sequences.fasta')
bt_infile = os.path.join(db_folder, 'binary_sequences.fasta')

test_1 = os.path.join(test_folder, 'test_seq', 'NC_002973.fna')
test_2 = os.path.join(test_folder, 'test_seq', 'NC_013768.fna')
test_3 = os.path.join(test_folder, 'test_seq', 'NC_017529.fna')
test_4 = os.path.join(test_folder, 'test_seq', 'NC_018588.fna')
test_5 = os.path.join(test_folder, 'test_seq', 'NC_018591.fna')


@pytest.fixture(scope='session')
def make_sero_db(tmpdir_factory):
    p = tmpdir_factory.mktemp('db')
    serodb = SerotypeDB(path_db=str(p),
                        infile=sero_infile)
    serodb.check_db()
    return serodb


@pytest.fixture(scope='session')
def make_bt_db(tmpdir_factory):
    p = tmpdir_factory.mktemp('db')
    btdb = SerotypeDB(path_db=str(p),
                      infile=bt_infile,
                      db_name='btsero',
                      title="Listeria Binary Typing BLAST DB")
    btdb.check_db()
    return btdb


def test_sample(make_sero_db, make_bt_db):
    sero_db = make_sero_db
    bt_db = make_bt_db
    blast = Blast()
    sample = Sample(test_1, blast, sero_db, bt_db)
    sample.get_serotype()
    sample.get_binarytype()
    print(sample)
    print(sample.serotype)
    print(sample.binarytype)
    assert 0
