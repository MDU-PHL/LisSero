"""
LisSero functions module
"""

import bz2
import gzip
import subprocess
import loguru

from .exceptions import (
    InvalidFASTAFormat,
    InvalidFASTADuplicateIdentifiers,
    InvalidFASTAEmptyFile,
    InvalidFASTAInvalidCharacters,
)

logger = loguru.logger


def is_fasta(fna):
    """
    Check if a file is a valid FASTA file
    :param fna: path to file
    :return: True if valid FASTA, False if not
    """
    # check if file is empty
    if os.stat(fna).st_size == 0:
        raise InvalidFASTAEmptyFile(f"{fna} is an empty file")
    # pylint: disable=c-extension-no-member
    return_code = FastaValidator.fasta_validator(fna)
    if return_code == 0:
        logger.info(f"{fna} is a valid FASTA file")
        return True
    elif return_code == 1:
        raise InvalidFASTAFormat(f"{fna} is not a valid FASTA file")
    elif return_code == 2:
        raise InvalidFASTADuplicateIdentifiers(f"{fna} contains duplicate identifiers")
    elif return_code == 4:
        return InvalidFASTAInvalidCharacters(f"{fna} contains invalid characters")
    else:
        return False


def open_fasta(fna):
    """
    Using the first 2 bytes of a file, determine if it is compressed or not with
    gzip or bzip2 or not, and return the appropriate file handle.
    """
    with open(fna, "rb") as f:
        magic = f.read(2)
        if magic == b"\x1f\x8b":
            return gzip.open(fna, "rt")
        elif magic == b"\x42\x5a":
            return bz2.open(fna, "rt")
        else:
            return open(fna, "rt", encoding="utf-8")


def run_blast(fna, db, blastn_path):
    """
    Given a fasta file and a blast database, run the blastn command and 
    return the results.
    First, must check if the fasta file is compressed or not .
    If compressed, created a tempfolder, and decompress the fasta file into it.
    Then, run the blast command.
    The blast command should look like this:
    /usr/local/bin/blastn -db /Users/andersgs/dev/mdu-phl/LisSero/lissero/db/lissero -ungapped -culling_limit 1 \
        -outfmt 6 qaccver saccver length slen pident -dust no \
            -query /Users/andersgs/dev/mdu-phl/LisSero/tests/test_seq/NC_018591.fna.gz
    This command should be able to run in concurrently with other blast commands
    """
    # Check if the fasta file is compressed or not
    with open_fasta(fna) as f:
        # Run the blast command
        blast_cmd = [
            blastn_path,
            "-db",
            db,
            "-ungapped",
            "-culling_limit",
            "1",
            "-outfmt",
            "6 qaccver saccver length slen pident",
            "-dust",
            "no",
            "-query",
            fna,
        ]
        blast_results = subprocess.run(
            blast_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if blast_results.returncode != 0:
            logger.critical(f"Error running blastn: {blast_results.stderr}")
            raise RuntimeError
        else:
            return blast_results.stdout.decode("utf-8")
