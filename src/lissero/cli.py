"""
The CLI module for LisSero

Use the argparse module, and create a function called parse_args() that will 
return the parsed arguments. 

The arguments should be:
-a/--assembly-id: the assembly id to use
-p/--pattern: The pattern to use to infer the the assembly id: options are filename
without the extension, the parent folder name, or a regex pattern
-c/--cpus: the number of cpus to use
-o/-outfile: the output filename, default sys.stdout
-h/--help: print the help message and exit
-v/--version: print the version and exit
-d/--database: the database to use, default lissero/data/serovar_db.fasta
FASTA: one or more FASTA files to process as pathlib.Path objects
"""

import argparse
import pathlib
import sys

from . import __version__ as version


def parse_args():
    """
    Parse the command line arguments
    """
    parser = argparse.ArgumentParser(
        description="LisSero: in silico serotyping of Listeria monocytogenes"
    )
    parser.add_argument(
        "-c", "--cpus", help="Number of concurrent jobs to run", type=int, default=1
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        help="Output filename (default: standard output)",
        default=sys.stdout,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Print the version and exit",
        action="version",
        version=f"%(prog)s {version}",
    )
    parser.add_argument(
        "-d",
        "--database",
        help="Serotype database to use",
        type=pathlib.Path,
        default=pathlib.Path("lissero/data/serovar_db.fasta"),
    )

    parser.add_argument("-a", "--assembly-id", type=str, help="Assembly id to use")

    parser.add_argument(
        "-p",
        "--pattern",
        dest="pattern",
        type=str,
        choices=["filename", "parent_folder", "regex"],
        help="the pattern to use to infer the the assembly id: options are filename"
        "without the extension, the parent folder name, or a regex pattern",
    )

    parser.add_argument(
        "FASTA", help="One or more FASTA files to process", type=pathlib.Path, nargs="+"
    )
    return parser.parse_args()
