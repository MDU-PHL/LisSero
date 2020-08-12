#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes

import click
import logging
import os
from pkg_resources import resource_filename

from lissero.scripts.Sample import Samples
from lissero.scripts.Sample import Sample
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
#fix control issue #16
@click.option("--controls", is_flag=True)
@click.option("--positive-control", is_flag=True)
@click.option("--negative-control", is_flag=True)

def run_lissero(serotype_db, min_id, min_cov, debug, fasta, controls, positive_control, negative_control):

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
    nega_pass = True
    pos_pass = True
    if controls or positive_control:
        pos_pass = run_controls("pos", sero_db=sero_db, blast=blast, sig_min_id = min_id, sg_min_cov = min_cov)
    if controls or negative_control:
        nega_pass = run_controls("neg", sero_db=sero_db, blast=blast, sig_min_id = min_id, sg_min_cov = min_cov)
    if nega_pass and pos_pass:
        samples = Samples(
            fasta, blast=blast, sero_db=sero_db, sg_min_id=min_id, sg_min_cov=min_cov
        )
        samples.run_typing()
        samples.simple_report()
    else:
        if not pos_pass:
            logging.error("Postive control Failed")
        if not nega_pass:
            loggint.error("Negative control Failed")
        logging.error("Lissero stopped due to Control test Failed")

def run_controls(type, sero_db, blast, sg_min_id, sg_min_cov):
    f = resource_filename("lissero", 'db')
    if type == "pos":
        pos_f = os.path.join(f, "controls", "GCF_000196035.1_ASM19603v1_genomic.fna")
        pos_sample = Sample(
                    pos_f,
                    blast=blast,
                    sero_db=sero_db,
                    sg_min_id=sg_min_id,
                    sg_min_cov=sg_min_cov,
                )
        pos_sample.get_serotype()
        if pos_sample.serotype.report["serotype"] == "1/2a, 3a":
            return True
        else:
            return False
    elif type == "neg":
        neg_f_1 = os.path.join(f, "controls", "GCF_000195795.1_ASM19579v1_genomic.fna")
        neg_f_2 = os.path.join(f, "controls", "GCF_000006945.2_ASM694v2_genomic.fna")
        neg_sample_1 = Sample(
                        neg_f_1,
                    blast=blast,
                    sero_db=sero_db,
                    sg_min_id=sg_min_id,
                    sg_min_cov=sg_min_cov,
                    )
        neg_sample_2 = Sample(
                        neg_f_2,
                    blast=blast,
                    sero_db=sero_db,
                    sg_min_id=sg_min_id,
                    sg_min_cov=sg_min_cov,
                    )
        neg_sample_1.get_serotype()
        neg_sample_2.get_serotype()
        if neg_sample_1.serotype.report["serotype"] == "Nontypeable" and neg_sample_2.serotype.report["serotype"] == "Nontypeable":
            return True
        else:
            return False
    else:
        return True
    
if __name__ == "__main__":
    run_lissero()
