'''
A class to deal with Blasting
'''

import subprocess
import shutil
import logging
import os
import re


class SubRunner:

    version_pat = re.compile(r'(\d)\.(\d)\.(\d)')

    def __init__(self, cmd, cmd_path=None):
        self.cmd = cmd
        if cmd_path is not None:
            self.cmd_path = os.path.realpath(cmd_path)
        else:
            self.cmd_path = shutil.which(self.cmd)
            if self.cmd_path is None:
                logging.critical(f"Could not find executable {self.cmd}")
                logging.critical("Please provide a path to the executable.")
                raise SystemError
        self.cmd_list = [self.cmd_path]

    def add_option(self, key, value=None):
        self.cmd_list += [str(key)]
        if value is not None:
            self.cmd_list += [str(value)]

    def version(self):
        self.add_option('-version')
        res = self.run()
        try:
            self.version_no = self.version_pat.findall(res.stdout)[0]
            major, minor, patch = self.version_no
        except:
            logging.critical(f"Something went wrong when parsing the version"
                             f" for {self.cmd}")
            raise SystemError
        logging.info(f'Found {self.cmd} version {major}.{minor}.{patch}')
        self.cmd_list = [self.cmd_path]

    def is_version(self, requirement):
        pass

    def run(self,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            retcode=0):
        p = subprocess.run(self.cmd_list,
                           stdout=stdout,
                           stderr=stderr,
                           encoding='utf8')
        if p.returncode != retcode:
            logging.critical(f"Failed to run {' '.join(self.cmd_list)}")
            raise SyntaxError
        return p

    def __str__(self):
        return ' '.join(self.cmd_list)


class Blast(SubRunner):
    def __init__(self, blast_path=None):
        super().__init__(cmd='blastn', cmd_path=blast_path)
        pass

    def add_db(self, path):
        path = os.path.realpath(path)
        self.add_option('-db', path)

    def add_query(self, path):
        path = os.path.realpath(path)
        self.add_option('-query', path)


class MakeBlastDB(SubRunner):
    def __init__(self, makeblastdb_path=None):
        super().__init__(cmd='makeblastdb', cmd_path=makeblastdb_path)
        pass
