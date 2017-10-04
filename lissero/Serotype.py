'''
A class to generate a Serotype

All Serotyping logic stays here.
'''

import os
import logging
import json
import datetime
import getpass
import hashlib
import shlex
import copy

from .Blast import MakeBlastDB


class Serotype:
    '''
    Serotyping of Listeria monocytogenes samples is performed throught the
    presence abscense of five genes.

    One gene must be present to ascert that the species is indeed Listeria
    monocytogenes (Prs). If the gene is not present, then Serotyping CANNOT
    proceed.

    Serogroup 1/2a, 3a requires the additional presence of: lmo0737

    Serogroup 1/2b, 3b, 7 requires the additional presence of: ORF2819

    Serogroup 1/2c, 3c requires the additional presence of: lmo1118 & lmo0737

    Serogroup 4b, 4d, 4e requires the additional presence of: ORF2110 & ORF2819

    Serogroup 4b, 4d, 4e* requires the additional presence of: ORF2110 & ORF2819 & lmo0737

    This creates a decision tree.

    What are the possible outputs?
        Alleles \in {'', Prs, lmo0737, lmo1118, ORF2819, ORF2110}

    if not Prs:
        stop
    elif lmo0737 and not (ORF2819 or ORF2110):
        if lmo1118:
            Serogroup 1/2c, 3c
        else:
            Serogroup 1/2a, 3a
    elif ORF2819 and not (lmo0737 or lmo1118):
        if ORF2110:
            Serogroup 4b, 4d, 4e
        else:
            Serogroup 1/2b, 3b, 7
    elif lmo0737 and ORF2819 and ORF2110:
        Serogroup 4b, 4d, 4e*
    else:
        Nontypable
    '''

    BLAST_OUTFMT = '6 qaccver saccver length slen pident'

    def __init__(self, blast_run, path_db,
                 cov=100,
                 pid=98):
        path_db = os.path.realpath(path_db)
        self.blast = copy.deepcopy(blast_run)
        self.blast.add_db(path_db)
        self.blast.add_option('-ungapped')
        self.blast.add_option('-culling_limit', 1)
        self.blast.add_option('-outfmt', self.BLAST_OUTFMT)
        self.blast.add_option('-dust', 'no')
        self.cov = cov
        self.pid = pid

    def _blast_run(self):
        self.blast_res = self.blast.run()

    def _blast_parse(self):
        self.full_matches = set()
        self.partial_matches = set()
        blast_matches = self.blast_res.stdout.strip().split('\n')
        for b in blast_matches:
            (qaccver,
             saccver,
             length,
             slen,
             pident) = b.split('\t')
            print(b)
            if float(pident) >= self.pid and\
               100*(float(length)/float(slen)) >= self.cov:
                self.full_matches.update([saccver.split('~~')[0]])
            else:
                pass

    def generate_serotype(self, query):
        self.blast.add_query(query)
        self._blast_run()
        self._blast_parse()
        pass


class SerotypeDB:
    def __init__(self, path_db,
                 infile=None,
                 db_name='lissero',
                 title='Listeria Serotyping BLAST DB',
                 makeblastdb_path=None,
                 force=False):
        self.title = title
        self.path_db = os.path.realpath(path_db)
        self.db_name = os.path.join(self.path_db, db_name)
        if infile is not None:
            self.infile = os.path.realpath(infile)
            self.mkdb = MakeBlastDB(makeblastdb_path=makeblastdb_path)
        else:
            self.infile = None
        self.force = force
        self.log_file = os.path.join(self.path_db, 'lissero_db.json')
        self.db_log = {}

    def check_db(self):
        if self.force and self.infile is not None:
            logging.info("Will rebuild database if one exists!")
            self._make_db()
            return
        elif os.path.exists(self.db_name+'.nhr'):
            self._load_log()
            logging.info(f"DB was created on {self.db_log['date_created']}")
            logging.info("DB is ready for use.")
        elif self.infile is None:
            logging.critical("There is no database, and I don't"
                             " have enough information to create one."
                             " Please add an input file for the DB"
                             " and run again.")
            raise IOError
        else:
            logging.warning(f"Did not find a DB at {self.path_db}")
            logging.warning("Will create a new one")
            self._make_db()

    def __str__(self):
        return self.db_name

    def version(self):
        return self.log_db['date created']

    def _load_log(self):
        if os.path.exists(self.log_file):
            fh = open(self.log_file, 'rt')
            self.log_db = json.load(fh)
            logging.info("Successfully loaded DB log!")
            fh.close()
        else:
            logging.warning("Did find a log file at {self.path_db}")

    def _save_log(self):
        fh = open(self.log_file, 'wt')
        json.dump(self.db_log, fh, indent=4)
        logging.info("Successfully saved log!")

    def _hash_file(self, filename):
        f = open(filename, 'rb')
        file_content = f.read()
        h = hashlib.sha256(file_content).hexdigest()
        f.close()
        return h

    def _make_db(self):
        self.db_log['date_created'] = datetime.datetime.today().isoformat()
        mkdb = self.mkdb
        mkdb.add_option('-dbtype', 'nucl')
        mkdb.add_option('-in', self.infile)
        mkdb.add_option('-parse_seqids')
        mkdb.add_option('-input_type', 'fasta')
        mkdb.add_option('-out', self.db_name)
        mkdb.add_option('-title', shlex.quote(self.title))
        mkdb.run()
        self.db_log['cmd'] = str(mkdb)
        self.db_log['creator'] = getpass.getuser()
        self.db_log['infile'] = {}
        self.db_log['infile']['path'] = self.infile
        self.db_log['infile']['sha256'] = self._hash_file(self.infile)
        self.db_log['title'] = self.title
        self._save_log()
        logging.info(f"Successfully created {self.db_name}")
