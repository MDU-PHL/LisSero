"""
This module contains the serotyping functions and data models
"""

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
