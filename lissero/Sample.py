'''
A sample class for LisSero
'''

import os


class Sample:
    def __init__(self, filename):
        self.filename = os.path.realpath(filename)
        pass

    def is_fasta(self):
        pass

    def get_serotype(self):
        pass

    def __str__(self):
        pass
