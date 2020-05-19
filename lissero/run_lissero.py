#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes

import click
import logging
import os

from lissero.scripts.Sample import Samples
from lissero.scripts.Blast import Blast
from lissero.scripts.Serotype import SerotypeDB
from .__init__ import __version__ as version

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"LisSero {version}")
    ctx.exit()

@click.command()
@click.option("-s", "--serotype_db", default=None, envvar="LISSERO_DB")
@click.option(
    "--min_id",
    default=95.0,
    help="Minimum percent identity to accept a match. [0-100]",
    show_default=True,
)
@click.option(
    "--min_cov",
    default=95.0,
    help="Minimum coverage of the gene to accept a match. [0-100]",
    show_default=True,
)
@click.option("--debug", is_flag=True)
@click.argument("fasta", nargs=-1, type=click.Path(), required=True)
#fix Version Issue #10
@click.option("--version", is_flag=True, callback=print_version, \
              expose_value=False, is_eager=True, help="Show Version Information")

def run_lissero(serotype_db, min_id, min_cov, debug, fasta):

    """
    In silico serogroup prediction for L. monocytogenes.
    Alleles: lmo1118, lmo0737, ORF2819, ORF2110, Prs

    References:

    * Doumith et al. Differentiation of the major Listeria monocytogenes
        serovars by multiplex PCR. J Clin Microbiol, 2004; 42:8; 3819-22

    """
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(filename='./lissero.log', level=log_level)
    #fix issue #11 and #12
    path_serodb = ""
    try:
        path_serodb = os.path.realpath(serotype_db)
    except:
        logging.error(f"Please provide a correct serotype db path or set correct PATH for LISSERO_DB")
        sys.exit()
    sero_db = SerotypeDB(path_db=path_serodb, db_type="serotype")
    sero_db.check_db()
    blast = Blast()
    samples = Samples(
        fasta, blast=blast, sero_db=sero_db, sg_min_id=min_id, sg_min_cov=min_cov
    )
    samples.run_typing()
    samples.simple_report()


if __name__ == "__main__":
    run_lissero()
