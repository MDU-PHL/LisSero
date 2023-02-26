"""
The main entry point module for LisSero

This module is the main entry point for LisSero. It is called by the lissero command.

It is also used by pyproject.toml to create the lissero command.

It imports the parse_args() function from lissero.cli, and calls it to parse the
command line arguments.

It uses the asyncio api to run main asynchronously to blast over each FASTA file
in parallel, while keeping the number of concurrent jobs to the number of cpus 
specified by the user.

The blast functions will be imported from lissero.func module
"""
import asyncio
import pathlib
import sys

from .cli import parse_args
from .func import blast, blast_parse


# The main function is the entry point for LisSero
def main():
    """
    The main entry point for LisSero
    """
    # Parse the command line arguments
    args = parse_args()

    # Create the asyncio event loop
    loop = asyncio.get_event_loop()

    # Create a list of tasks to run
    tasks = []

    # For each FASTA file
    for fasta in args.fasta:
        # Create a task to run the blast function
        task = loop.create_task(blast(fasta, args.cpus, args.database))
        # Add the task to the list of tasks
        tasks.append(task)

    # Run the tasks and wait for them to complete
    loop.run_until_complete(asyncio.wait(tasks))

    # Create a list of tasks to run
    tasks = []

    # For each task
    for task in tasks:
        # Get the result of the task
        result = task.result()
        # Create a task to run the blast_parse function
        task = loop.create_task(blast_parse(result, args.outfile))
        # Add the task to the list of tasks
        tasks.append(task)

    # Run the tasks and wait for them to complete
    loop.run_until_complete(asyncio.wait(tasks))

    # Close the event loop
    loop.close()
