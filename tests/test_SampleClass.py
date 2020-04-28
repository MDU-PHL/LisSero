import pytest
import os
from lissero.scripts.Serotype import SerotypeDB
from lissero.scripts.Blast import Blast
from lissero.scripts.Sample import Sample
from lissero.scripts.Sample import Samples

BLAST_OUTFMT = '6 qaccver saccver length slen pident'

test_folder = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(os.path.dirname(test_folder), 'db')

test_1 = os.path.join(test_folder, 'test_seq', 'NC_002973.fna')
test_2 = os.path.join(test_folder, 'test_seq', 'NC_013768.fna')
test_3 = os.path.join(test_folder, 'test_seq', 'NC_017529.fna')
test_4 = os.path.join(test_folder, 'test_seq', 'NC_018588.fna')
test_5 = os.path.join(test_folder, 'test_seq', 'NC_018591.fna')


@pytest.fixture(scope='session')
def make_sero_db(tmpdir_factory):
    p = tmpdir_factory.mktemp('db')
    serodb = SerotypeDB(path_db=str(p),
                        db_type='serotype')
    serodb.check_db()
    return serodb

"""
@pytest.fixture(scope='session')
def make_bt_db(tmpdir_factory):
    p = tmpdir_factory.mktemp('db')
    btdb = SerotypeDB(path_db=str(p),
                      db_type='binary_type',
                      db_name='btsero',
                      title="Listeria Binary Typing BLAST DB")
    btdb.check_db()
    return btdb
"""

#@pytest.mark.skip(reason="Not ready")
def test_sample(make_sero_db):
#def test_sample(make_sero_db, make_bt_db):
    sero_db = make_sero_db
    bt_db = make_bt_db
    blast = Blast()
    #delete bt type parameter
    #sample = Sample(test_1, blast, sero_db, bt_db)
    sample = Sample(test_1, blast, sero_db)
    sample.get_serotype()
    #sample.get_binarytype()
    # print(sample)
    # print(sample.serotype)
    # print(sample.binarytype)
    assert 1


#@pytest.mark.skip(reason="Not ready")
def test_class_samples(make_sero_db):
#def test_class_samples(make_sero_db, make_bt_db):
    sero_db = make_sero_db
    #bt_db = make_bt_db
    blast = Blast()
    samples = Samples([test_1,
                       test_2,
                       test_3,
                       test_4,
                       test_5],
                      blast,
                      sero_db)
                      #bt_db)
    samples.run_typing()
    # print(samples)
    """
    for s in samples.samples:
        # print(s.serotype)
        print(s.binarytype)
    samples.simple_report()"""
    assert 1
