'''
A sample class for LisSero
'''

import os

from .Serotype import Serotype
from .Serotype import BinaryType


class Sample:
    def __init__(self, filename, blast, sero_db, bt_db):
        self.filename = os.path.realpath(filename)
        self.serotype = Serotype(blast, sero_db)
        self.binarytype = BinaryType(blast, bt_db)

    def is_fasta(self):
        pass

    def get_serotype(self):
        self.serotype.generate_type(self.filename)

    def get_binarytype(self):
        self.binarytype.generate_type(self.filename)

    def __str__(self):
        # try:
        #     string = f"{self.filename}"\
        #              f"\tSEROTYPE: {self.serotype.report['serotype']}"\
        #              f"\tBINARYTYPE: {self.serotype.report['binarytype']}"
        # except:
        #     string = ''
        # return string
        string = f"{self.filename}"\
                 f"\tSEROTYPE: {self.serotype.report['serotype']}"\
                 f"\tBINARYTYPE: {self.binarytype.report['binarytype']}"
        return string


class Samples:
    def __init__(self):
        pass
