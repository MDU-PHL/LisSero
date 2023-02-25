"""
This module contains the serotyping functions and data models
"""

import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Data models

class Result(Enum):
    """
    An enum to represent the results of a serotype
    """
    FULL = 1
    PARTIAL = 2
    NONE = 3


class Comment(Enum):
    """
    An enum to represent the comments for a serotype
    """
    NONE = 1
    NO_PRS = 2
    NO_SEROTYPE = 3
    UNUSUAL_4B = 4

class Serogroup(Enum):
    """
    An enum to represent the serogroups
    """
    ONE_TWO_A = 1
    ONE_TWO_B = 2
    ONE_TWO_C = 3
    THREE_A = 4
    THREE_B = 5
    THREE_C = 6
    FOUR_B = 7
    FOUR_D = 8
    FOUR_E = 9
    SEVEN = 10

@dataclass
class BlastHit:
    """
    A model to contain the blast hits for a sample
    """
    prs: Result
    lmo0737: Result
    lmo1118: Result
    orf2110: Result
    orf2819: Result


@dataclass
class Serotype:
    """
    A model to contain the serotype information for the a sample
    """
    sample_id: str
    fasta_file: str
    prs: bool
    lmo0737: bool
    lmo1118: bool
    orf2110: bool
    orf2819: bool
    blast_results: BlastHit
    serotype: Optional[Serogroup] = None
    comment: Optional[Comment] = None


# Functions

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
        blast_results = subprocess.run(blast_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if blast_results.returncode != 0:
            logger.critical(f"Error running blastn: {blast_results.stderr}")
            raise RuntimeError
        else:
            return blast_results.stdout.decode("utf-8")