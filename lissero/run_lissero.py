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
              envvar='LISSERO_DB')
@click.option("-b", "--binarytype_db", default=None,
              envvar='LISBT_DB')
@click.option("--bt_min_id", default=90)
@click.option("--bt_min_cov", default=95)
@click.option("--sg_min_id", default=95)
@click.option("--sg_min_cov", default=95)
@click.option("--debug", is_flag=True)
@click.argument("fasta", nargs=-1,  required=True)
def run_lissero(serotype_db, binarytype_db,
                sg_min_id, sg_min_cov,
                bt_min_id, bt_min_cov,
                debug,
                fasta):
    '''
    In silico serogroup prediction for L. monocytogenes.
    Alleles: lmo1118, lmo0737, ORF2819, ORF2110, Prs

    In silico binary type prediction for L. monocytogenes.
    Alleles: 1, 2, 4, 8, 16, 32, 64, 128

    References:

    * Doumith et al. Differentiation of the major Listeria monocytogenes
        serovars by multiplex PCR. J Clin Microbiol, 2004; 42:8; 3819-22

    * Huang et al. Binary typing of *Listeria monocytogenes* isolates from
        patients and food through multiplex PCR and reverse line hybridisation.
        SA, Australia, 2007; 136–137.

    '''
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)
    path_serodb = os.path.realpath(serotype_db)
    path_btdb = os.path.realpath(binarytype_db)
    sero_db = SerotypeDB(path_db=path_serodb,
                         db_type='serotype')
    sero_db.check_db()
    bt_db = SerotypeDB(path_db=path_btdb,
                       db_type='binary_type',
                       db_name='lisbt')
    bt_db.check_db()
    blast = Blast()
    samples = Samples(fasta,
                      blast=blast,
                      sero_db=sero_db,
                      bt_db=bt_db,
                      sg_min_id=sg_min_id,
                      sg_min_cov=sg_min_cov,
                      bt_min_id=bt_min_id,
                      bt_min_cov=bt_min_cov)
    samples.run_typing()
    samples.simple_report()


if __name__ == "__main__":
    run_lissero()
