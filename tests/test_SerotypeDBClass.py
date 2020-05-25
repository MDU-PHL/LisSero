import pytest
import os
from lissero.scripts.Serotype import SerotypeDB
from lissero.scripts.Serotype import Serotype
from lissero.scripts.Serotype import report_maker
#from lissero.Serotype import BinaryType
from lissero.scripts.Blast import Blast

BLAST_OUTFMT = '6 qaccver saccver length slen pident'

test_folder = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(os.path.dirname(test_folder), 'db')
sero_infile = 'sequences.fasta'
#bt type
#bt_infile = 'binary_sequences.fasta'

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
test bt db
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

def test_check_db(make_sero_db):
    db = make_sero_db
    assert os.path.exists(db.db_name+'.nhr')


def test_infile_against_db(make_sero_db):
    db = make_sero_db
    blast = Blast()
    blast.add_db(db.db_name)
    blast.add_option('-ungapped')
    blast.add_option('-culling_limit', 1)
    blast.add_option('-outfmt', BLAST_OUTFMT)
    blast.add_option('-dust', 'no')
    blast.add_query(db.infile)
    res = blast.run()
    assert res.returncode == 0


def test_seq_against_sero_db(make_sero_db):
    db = make_sero_db
    blast = Blast()
    serotype = Serotype(blast, db)
    serotype.generate_type(test_1)
    assert {'ORF2110', 'ORF2819', 'PRS'} == serotype.full_matches

@pytest.mark.parametrize("test_input, expected",
    [(["PRS"], "Nontypeable"), 
    ([], "Nontypeable")
    ],
    )
def test_report_maker(test_input, expected):
    serotype = reprot_maker(test_input)["serotype"]
    assert serotype == expected

"""
test bt db
def test_seq_against_bt_db(make_bt_db):
    db = make_bt_db
    blast = Blast()
    binarytype = BinaryType(blast, db)
    binarytype.generate_type(test_1)
    assert '254' == binarytype.report['binarytype']
"""
