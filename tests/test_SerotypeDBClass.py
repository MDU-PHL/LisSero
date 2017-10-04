import pytest
import os
from lissero.Serotype import SerotypeDB
from lissero.Serotype import Serotype
from lissero.Blast import Blast

BLAST_OUTFMT = '6 qaccver saccver length slen pident'

test_folder = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(os.path.dirname(test_folder), 'db')
infile = os.path.join(db_folder, 'sequences.fasta')

test_1 = os.path.join(test_folder, 'test_seq', 'NC_002973.fna')
test_2 = os.path.join(test_folder, 'test_seq', 'NC_013768.fna')
test_3 = os.path.join(test_folder, 'test_seq', 'NC_017529.fna')
test_4 = os.path.join(test_folder, 'test_seq', 'NC_018588.fna')
test_5 = os.path.join(test_folder, 'test_seq', 'NC_018591.fna')


@pytest.fixture(scope='session')
def make_db(tmpdir_factory):
    p = tmpdir_factory.mktemp('db')
    serodb = SerotypeDB(path_db=str(p),
                        infile=infile)
    serodb.check_db()
    return serodb


def test_check_db(make_db):
    db = make_db
    assert os.path.exists(db.db_name+'.nhr')


def test_infile_against_db(make_db):
    db = make_db
    blast = Blast()
    blast.add_db(db.db_name)
    blast.add_option('-ungapped')
    blast.add_option('-culling_limit', 1)
    blast.add_option('-outfmt', BLAST_OUTFMT)
    blast.add_option('-dust', 'no')
    blast.add_query(infile)
    res = blast.run()
    assert res.returncode == 0


def test_seq_against_db(make_db):
    db = make_db
    blast = Blast()
    serotype = Serotype(blast, db.db_name)
    serotype.generate_serotype(test_1)
    assert {'ORF2110', 'ORF2819', 'Prs'} == serotype.full_matches
