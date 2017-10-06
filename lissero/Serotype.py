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
import pkg_resources

from .Blast import MakeBlastDB


SEROTYPE_FASTA = 'db/sequences.fasta'
BINARYTYPE_FASTA = 'db/binary_sequences.fasta'


class Typing:

    BLAST_OUTFMT = '6'
    OUTPUT_HEADER = ['ID', 'TYPE',
                     'DB_VERSION']

    def __init__(self, blast_run, db,
                 cov=100,
                 pid=100):
        self.db_version = db.version
        path_db = os.path.realpath(db.db_name)
        self.blast = copy.deepcopy(blast_run)
        self.blast.add_db(path_db)
        self.blast.add_option('-ungapped')
        self.blast.add_option('-culling_limit', 1)
        self.blast.add_option('-outfmt', self.BLAST_OUTFMT)
        self.blast.add_option('-dust', 'no')
        self.cov = cov
        self.pid = pid

    def __str__(self):
        try:
            string = json.dumps(self.report, indent=4)
        except:
            string = '{}'
        return string

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
            if float(pident) >= self.pid and\
               100*(float(length)/float(slen)) >= self.cov:
                self.full_matches.update([saccver.split('~~')[0]])
            else:
                self.partial_matches.update([saccver.split('~~')[0]])

    def tab_report(self, header=True, sep=','):
        if header:
            print(sep.join(self.OUTPUT_HEADER))
        out = []
        for field in self.OUTPUT_HEADER:
            out += [self.report[field.lower()]]
        print(sep.join(out))

    def csv_report(self, header=True):
        self.tab_report(sep=',', header=header)

    def tsv_report(self, header=True):
        self.tab_report(sep='\t', header=header)


class Serotype(Typing):
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
    OUTPUT_HEADER = ['ID', 'SEROTYPE',
                     'Prs', 'lmo0737',
                     'lmo1118', 'ORF2110',
                     'ORF2819', 'COMMENT',
                     'DB_VERSION']

    def __init__(self, blast_run, db,
                 cov=100,
                 pid=98):
                super().__init__(blast_run=blast_run,
                                 db=db,
                                 cov=cov,
                                 pid=pid)

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
            obs_pid = float(pident)
            obs_cov = 100 * (float(length)/float(slen))
            if obs_pid >= self.pid and obs_cov >= self.cov:
                self.full_matches.update([saccver.split('~~')[0].upper()])
            else:
                self.partial_matches.update([saccver.split('~~')[0].upper()])

    def generate_type(self, query):
        report = {'prs': None,
                  'lmo0737': None,
                  'lmo1118': None,
                  'orf2110': None,
                  'orf2819': None}
        self.blast.add_query(query)
        self._blast_run()
        self._blast_parse()
        for gene in report:
            if gene.upper() in self.full_matches:
                report[gene] = 'FULL MATCH'
            elif gene.upper() in self.partial_matches:
                report[gene] = 'PARTIAL MATCH'
            else:
                report[gene] = 'NOT FOUND'
        if 'PRS' not in self.full_matches:
            report['serotype'] = 'Nontypable'
            report['comment'] = 'No Prs found'
        elif 'LMO0737' in self.full_matches and\
             'ORF2819' not in self.full_matches and\
             'ORF2110' not in self.full_matches:
            if 'LMO1118' in self.full_matches:
                report['serotype'] = '1/2c, 3c'
                report['comment'] = None
            else:
                report['serotype'] = '1/2a, 3a'
                report['comment'] = None
        elif 'ORF2819' in self.full_matches and\
             'LMO0737' not in self.full_matches and\
             'LMO1118' not in self.full_matches:
            if 'ORF2110' in self.full_matches:
                report['serotype'] = '4b, 4d, 4e'
                report['comment'] = None
            else:
                report['serotype'] = "1/2b, 3b, 7"
                report['comment'] = None
        elif 'LMO0737' in self.full_matches and\
             'ORF2819' in self.full_matches and\
             'ORF2110' in self.full_matches:
            report['serotype'] = '4b, 4d, 4e*'
            report['comment'] = 'Unusual 4b with lmo0737'
        else:
            report['serotype'] = 'Nontypable'
            report['comment'] = 'No combination of fully matched genes'\
                                ' resulted in a known serotype.'
        report['id'] = query
        report['db_version'] = self.db_version()
        self.report = report
        logging.debug(report)


class BinaryType(Typing):
    '''
    Listeria Binary Typing.

    The Binary Type is the sum of the individual gene numbers.

    For example, an isolate with genes 1, 4, and 32 would have a
    binary type of 37.
    '''

    BLAST_OUTFMT = '6 qaccver saccver length slen pident'
    OUTPUT_HEADER = ['ID', 'BINARYTYPE',
                     '1', '2',
                     '4', '8',
                     '16', '32',
                     '64', '128',
                     'COMMENT',
                     'DB_VERSION']
    DEFAULT_REPORT = {'blast_hits': [],
                      'consensus': None,
                      'blast_summary': None,
                      'comments': None,
                      'qualifier': None
                      }

    GENES = ['1', '2', '4',
             '8', '16', '32',
             '64', '128']

    def __init__(self, blast_run, db,
                 cov=95,
                 pid=95):
                super().__init__(blast_run=blast_run,
                                 db=db,
                                 cov=cov,
                                 pid=pid)

    def _blast_parse(self):
        self.blast_hits = []
        blast_matches = self.blast_res.stdout.strip().split('\n')
        for b in blast_matches:
            blast_json = dict(
                zip(
                    ['query_id',
                     'hit_id',
                     'alignment_length',
                     'hit_length',
                     'percent_id'],
                    b.split('\t')
                )
            )
            blast_json['alignment_length'] = float(blast_json['alignment_length'])
            blast_json['hit_length'] = float(blast_json['hit_length'])
            blast_json['percent_id'] = float(blast_json['percent_id'])
            blast_json['coverage'] = 100 * (blast_json['alignment_length']/blast_json['hit_length'])
            blast_json['gene'] = int(blast_json['hit_id'].split('~~')[0])
            if blast_json['percent_id'] >= self.pid and blast_json['coverage'] >= self.cov:
                blast_json['match'] = 'FULL'
            else:
                blast_json['match'] = 'PARTIAL'
            self.blast_hits += [blast_json]

    def _map_hits_to_genes(self):
        report = {g: copy.deepcopy(self.DEFAULT_REPORT) for g in self.GENES}
        for hit in self.blast_hits:
            gene = str(hit['gene'])
            report[gene]['blast_hits'] += [hit]
        self.report = report

    def _parse_multiple_hits(self, hits):
        n_full_hits = 0
        n_partial_matches = 0
        full_hits = []
        for hit in hits:
            if hit['match'] == 'FULL':
                n_full_hits += 1
                full_hits += [hit]
            else:
                n_partial_matches += 1
        if n_full_hits == 0:
            return (f'MULTIPLE PARTIAL MATCHES ({n_partial_matches})',
                    None,
                    '%',
                    "MULTIPLE PARTIAL COPIES OF ALLELE,"
                    " NOT COUNTED TOWARDS BINARY TYPE"
                    )
        elif n_full_hits == 1:
            return('FULL MATCH',
                   full_hits[0]['gene'],
                   None,
                   None)
        else:
            return(f'MULTIPLE FULL MATCHES ({n_full_hits})',
                   None,
                   '^',
                   "MULTIPLE FULL COPIES OF ALLELE,"
                   " NOT COUNTED TOWARDS BINARY TYPE"
                   )

    def _check_mapping(self):
        for g in self.report:
            tmp = self.report[g]
            n_hits = len(tmp['blast_hits'])
            if n_hits == 0:
                tmp['blast_summary'] = 'NOT FOUND'
            elif n_hits == 1:
                if tmp['blast_hits'][0]['match'] == 'FULL':
                    tmp['blast_summary'] = 'FULL MATCH'
                    tmp['consensus'] = tmp['blast_hits'][0]['gene']
                else:
                    tmp['blast_summary'] = 'PARTIAL MATCH'
                    tmp['consensus'] = tmp['blast_hits'][0]['gene']
                    tmp['qualifier'] = '~'
                    tmp['comment'] = "PARTIAL ALLELES FOUND, NOT COUNTED"\
                                     " TOWARDS BINARY TYPE"
            else:
                (tmp['blast_summary'],
                 tmp['consensus'],
                 tmp['qualifier'],
                 tmp['comment']) = self._parse_multiple_hits(tmp['blast_hits'])

    def _type(self):
        binarytype = 0
        for g in self.report:
            tmp = self.report[g]
            if tmp['blast_summary'] == 'FULL MATCH':
                binarytype += tmp['consensus']
        return binarytype

    def _qualifiers(self):
        qualifiers = ''
        for g in self.report:
            tmp = self.report[g]
            if tmp['qualifier'] is not None:
                qualifiers += tmp['qualifier']
        qualifiers = list(set(qualifiers))
        qualifiers = ''.join(qualifiers)
        return qualifiers

    def _comments(self):
        comments = []
        for g in self.report:
            tmp = self.report[g]
            if tmp["comments"] is not None:
                comments += [tmp['comment']]
        if len(comments) == 0:
            comments = ''
        else:
            comments = ';'.join(comments)
        return comments

    def generate_type(self, query):
        self.blast.add_query(query)
        self._blast_run()
        self._blast_parse()
        self._map_hits_to_genes()
        self._check_mapping()
        binarytype = self._type()
        qualifiers = self._qualifiers()
        self.report["comments"] = self._comments()
        self.report['binarytype'] = f'{binarytype}{qualifiers}'
        self.report['id'] = query
        self.report['db_version'] = self.db_version()
        logging.debug(self.report)


class SerotypeDB:
    def __init__(self, path_db,
                 db_type,
                 db_name='lissero',
                 title='Listeria Serotyping BLAST DB',
                 makeblastdb_path=None,
                 force=False):
        self.title = title
        self.path_db = os.path.realpath(path_db)
        self.db_name = os.path.join(self.path_db, db_name)
        self.mkdb = MakeBlastDB(makeblastdb_path=makeblastdb_path)
        if db_type == 'serotype':
            self.infile = pkg_resources.resource_filename('lissero', SEROTYPE_FASTA)
        elif db_type == 'binary_type':
            self.infile = pkg_resources.resource_filename('lissero', BINARYTYPE_FASTA)
        else:
            logging.critical(f'I don\'t understand db_type = {db_type}')
            raise IOError
        self.force = force
        self.log_file = os.path.join(self.path_db, db_name+'_db.json')
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
        return self.db_log['date_created']

    def _load_log(self):
        if os.path.exists(self.log_file):
            fh = open(self.log_file, 'rt')
            self.db_log = json.load(fh)
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
