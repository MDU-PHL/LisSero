'''
A sample class for LisSero
'''

import os
import logging

from .Serotype import Serotype
from .Serotype import BinaryType


class Sample:
    def __init__(self, filename,
                 blast,
                 sero_db,
                 sg_min_id,
                 sg_min_cov,
                 bt_db,
                 bt_min_id,
                 bt_min_cov
                 ):
        self.id = filename
        self.filename = os.path.realpath(filename)
        self.serotype = Serotype(blast,
                                 sero_db,
                                 pid=sg_min_id,
                                 cov=sg_min_cov)
        self.binarytype = BinaryType(blast,
                                     bt_db,
                                     pid=bt_min_id,
                                     cov=bt_min_cov)

    def is_fasta(self):
        pass

    def get_serotype(self):
        logging.info(f'Serotyping: {self.id}')
        self.serotype.generate_type(self.filename)

    def get_binarytype(self):
        logging.info(f'Binary Typing: {self.id}')
        self.binarytype.generate_type(self.filename)

    def __str__(self):
        try:
            string = f"{self.id}"\
                     f"\tSEROTYPE: {self.serotype.report['serotype']}"\
                     f"\tBINARYTYPE: {self.binarytype.report['binarytype']}"
        except:
            string = ''
        return string


class Samples:

    SIMPLE_HEADER = ['ID', 'SEROTYPE', 'BINARYTYPE']

    def __init__(self, filenames,
                 blast,
                 sero_db,
                 sg_min_id,
                 sg_min_cov,
                 bt_db,
                 bt_min_id,
                 bt_min_cov):
        self.filenames = filenames
        self.blast = blast
        self.sero_db = sero_db
        self.bt_db = bt_db
        self.sg_min_id = sg_min_id
        self.sg_min_cov = sg_min_cov
        self.bt_min_id = bt_min_id
        self.bt_min_cov = bt_min_cov

    def _create_sample(self):
        self.samples = []
        for f in self.filenames:
            self.samples += [Sample(f,
                                    blast=self.blast,
                                    sero_db=self.sero_db,
                                    bt_db=self.bt_db,
                                    sg_min_id=self.sg_min_id,
                                    sg_min_cov=self.sg_min_cov,
                                    bt_min_id=self.bt_min_id,
                                    bt_min_cov=self.bt_min_cov)]

    def _run_typing(self, func):
        if func == 'serotype':
            for f in self.samples:
                f.get_serotype()
        elif func == 'binarytype':
            for f in self.samples:
                f.get_binarytype()
        else:
            logging.critical(f"Unknown function {func}")
            raise RuntimeError

    def run_typing(self):
        self._create_sample()
        self._run_typing("serotype")
        self._run_typing("binarytype")

    def simple_report(self, header=True):
        print('\t'.join(self.SIMPLE_HEADER))
        for sample in self.samples:
            sample_id = sample.serotype.report['id']
            serotype = sample.serotype.report['serotype']
            binarytype = sample.binarytype.report['binarytype']
            print('\t'.join([sample_id, serotype, binarytype]))

    def __str__(self):
        return f'Typing {len(self.filenames)} samples'
