#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes

import click
import logging
import os

from .Sample import Samples
from .Blast import Blast
from .Serotype import SerotypeDB


@click.command()
@click.option("-s", "--serotype_db", default=None,
              envar='LISSERO_DB')
@click.option("-b", "--binarytype_db", default=None,
              envar='LISBT_DB')
@click.argument("fasta", nargs=-1)
def run_lissero(serotype_db, binarytype_db, fasta):
    '''
    In silico serogroup prediction for L.monocytogenes
    Alleles: lmo1118, lmo0737, ORF2819, ORF2110, Prs
    run_lissero FASTA [FASTA, [FASTA, [...]]]

    Ref: Doumith et al. Differentiation of the major Listeria monocytogenes
        serovars by multiplex PCR. J Clin Microbiol, 2004; 42:8; 3819-22
    '''
    logging.basicConfig(level=logging.INFO)
    path_serodb = os.path.realpath(serotype_db)
    path_btdb = os.path.realpath(binarytype_db)
    sero_db = SerotypeDB(path_db=path_serodb,
                         db_type='serotype')
    bt_db = SerotypeDB(path_db=path_btdb,
                       db_type='binarytype')
    blast = Blast()
    samples = Samples(fasta,
                      blast=blast,
                      sero_db=sero_db,
                      bt_db=bt_db)
    samples.run_typing()
    samples.simple_report()


if __name__ == "__main__":
    run_lissero()
