#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes
import sys
import logging
import os

import click
import loguru
import pkg_resources
from Bio import SeqIO

from lissero.scripts.Sample import Samples
from lissero.scripts.Blast import Blast
from lissero.scripts.Serotype import SerotypeDB
from .__init__ import __version__ as version

logger = loguru.logger

DEFAULT_DB = pkg_resources.resource_filename("lissero", "db")


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"LisSero {version}")
    ctx.exit()


def is_fasta(filename):
    """
    There are no real FASTA validators out there.
    This is the best I could come up with. If the
    file is empty or does not contain any FASTA records
    the parser will return an empty generator which will
    return a StopIteration exception when running `next(gen)`.
    But, there is another case where the file starts with
    a `>`, and thus the generator works, but it returns an
    empty record, thus the `len(rec)) > 0.

    Args:
        filename: FASTA input name

    Returns:
        boolean: true if it looks like a FASTA false otherwise.
    """
    gen = SeqIO.parse(filename, "fasta")
    try:
        rec = next(gen)
        return len(rec) > 0
    except StopIteration:
        return False
    except Exception as e:
        logger.error(e)
        sys.exit(1)

@click.command()
@click.help_option("-h", "--help")
@click.option("-s", "--serotype_db", default=DEFAULT_DB, envvar="LISSERO_DB", show_default=True)
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
@click.option("--logfile", help="Save log to a file instead of printing to stderr", default="")
@click.argument("fasta", nargs=-1, type=click.Path(exists=True), required=True)
# fix Version Issue #10
@click.option("--version", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show Version Information")
def run_lissero(serotype_db, min_id, min_cov, debug, logfile, fasta):
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

    if logfile != "":
        logger.remove()
        logger.add(logfile, level=log_level)
    else:
        logger.remove()
        logger.add(sys.stderr, level=log_level)

    all_fasta = all([is_fasta(fna) for fna in fasta])
    if not all_fasta:
        logger.error("One or more input files do not appear to be "
                     "valid FASTA.")
        sys.exit(1)

    try:
        path_serodb = os.path.realpath(serotype_db)
    except TypeError as e:
        logger.error(f"Please provide a valid path for serotype db path or set correct PATH for LISSERO_DB")
        sys.exit(1)
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
