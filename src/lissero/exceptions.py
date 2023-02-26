"""
Custom exceptions for lissero
"""


# pylint: disable=unnecessary-pass
class InvalidFASTAFormat(Exception):
    """
    Exception raised when a FASTA file is invalid because it does not contain
    a first line starting with '>'
    """

    pass


class InvalidFASTADuplicateIdentifiers(Exception):
    """
    Exception raised when a FASTA file is invalid because it contains duplicate
    identifiers
    """

    pass


class InvalidFASTAEmptyFile(Exception):
    """
    Exception raised when a FASTA file is invalid because it is empty
    """

    pass


class InvalidFASTAInvalidCharacters(Exception):
    """
    Exception raised when a FASTA file is invalid because it contains invalid
    characters (not A, C, G, T, N, a, c, g, t, n)
    """

    pass
