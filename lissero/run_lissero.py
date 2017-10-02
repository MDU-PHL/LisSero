#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes

import click
import sys
import os
import subprocess
import logging

from Sample import Sample

@click.command()
@click.option("fasta", nargs=-1)
def run_lissero():
    '''
    In silico serogroup prediction for L.monocytogenes
    Alleles: lmo1118, lmo0737, ORF2819, ORF2110, Prs
    run_lissero FASTA [FASTA, [FASTA, [...]]]

    Ref: Doumith et al. Differentiation of the major Listeria monocytogenes
        serovars by multiplex PCR. J Clin Microbiol, 2004; 42:8; 3819-22
    '''
    pass


if __name__ == "__main__":
    run_lissero()





# Check files in FASTA format
def facheck(f):
    if os.path.isfile(f) == False:
        print 'ERROR: Cannot find "%(f)s". Check file exists.' % globals()
        return 1
    s = open(f, 'r')
    if s.read(1) != '>':
        print 'ERROR: "%(f)s" does not appear to be in FASTA format.' % globals()
        return 1
    s.close()

# Print full header
def headerfull():
    print '-----------------------'
    print 'STRAIN:' + '\t' + f
    print '-----------------------'

# Print standard header
def headerstd():
    print 'STRAIN' + '\t' + 'isSEROTYPE' + '\t' + 'AMPLICONS'

# Check EMBOSS primersearch installed and running correctly
def which(program):
    import os
    def checkexe(exe):
        return os.path.isfile(exe) and os.access(exe, os.X_OK)
    exe, name = os.path.split(program)
    if exe:
        if checkexe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exepath = os.path.join(path, program)
            if checkexe(exepath):
                return exepath
    return None

if which('primersearch') == None:
    print 'ERROR: Check EMBOSS PrimerSearch is installed and in your $PATH.'
    progexit(1)

# Set path to primers
if args.primers:
    primers = str(args.primers)
else:
    primers = os.path.dirname(os.path.realpath(sys.argv[0])) + "/../db/primers.tab"

# Load dictionaries
ampsize = {16:906, 8:691, 4:471, 2:597, 1:370}		# Dictionary for expected amplicon size

# Load the serotype labels
serotype = {}
serotype_file = os.path.dirname(os.path.realpath(sys.argv[0])) + "/../db/serotypes.tab"
with open(serotype_file) as f:
        for line in f:
                col = line.rstrip('\n').split('\t')
                serotype[ int(col[0]) ] = col[1]

# Print detailed output from PrimerSearch if --full option set
if args.ampseq == 0 and args.full:
    for f in args.fasta:
        if facheck(f) == 1:
            continue
        headerfull()
        # Run EMBOSS PrimerSearch (BioPython module deprecated)
        proc = subprocess.Popen(['primersearch', '-seqall', f, '-infile', primers, '-mismatchpercent', args.mismatch, '-stdout', '-auto'], stdout=subprocess.PIPE)
        print proc.stdout.read()
    progexit(0)

# Print amplicon sequence from Jim Kent's isPcr if --ampseq option set
elif args.full == 0 and args.ampseq:
    for f in args.fasta:
        if facheck(f) == 1:
            continue
        headerfull()
        # Run isPcr by Jim Kent
        proc = subprocess.Popen(['isPcr', f, primers, 'stdout', '-minPerfect=3'], stdout=subprocess.PIPE)
        print proc.stdout.read()
    progexit(0)

# Both --full and --ampseq
elif args.full and args.ampseq:
    for f in args.fasta:
        if facheck(f) == 1:
            continue
        headerfull()
        # Run EMBOSS PrimerSearch (BioPython module deprecated)
        proc = subprocess.Popen(['primersearch', '-seqall', f, '-infile', primers, '-mismatchpercent', args.mismatch, '-stdout', '-auto'], stdout=subprocess.PIPE)
        print proc.stdout.read()
        # Run isPcr by Jim Kent
        proc = subprocess.Popen(['isPcr', f, primers, 'stdout', '-minPerfect=3'], stdout=subprocess.PIPE)
        print proc.stdout.read()
    progexit(0)

# Print output in tab-separated format
else:
    headerstd()
    for f in args.fasta:
        if facheck(f) == 1:
            continue
        # List of amplified products
        products = []
        # Run EMBOSS PrimerSearch (BioPython module deprecated)
            proc = subprocess.Popen(['primersearch', '-seqall', f, '-infile', primers, '-mismatchpercent', args.mismatch, '-stdout', '-auto'], stdout=subprocess.PIPE)
        for line in proc.stdout:
            if not line.strip():						# Ignore blank lines
                continue
            if line.startswith("Primer name"):			# Retrieve primer name
                name = int(line.split()[2])
            if line.startswith("\tAmplimer length"):	# Check amplicon length against expected size in dictionary
                length = int(line.split()[2])			# Only include product if +/- 6 bp
                predicted = ampsize[name]
                if length > (predicted - 6) and length < (predicted + 6):
                    products.append(name)

        a = set(products)					# Only count gene duplicates once
        b = map(int, a)						# Ensure all values are integers
        stsum = sum(b)						# Add values of gene products for serotype
        c = serotype[stsum]

        if (stsum == 4) or (stsum == 5):
            print f + '\t' + '1/2b,3b,7' + '\t' + c
        elif (stsum == 24) or (stsum == 25) or (stsum == 17) or (stsum == 18):
            print f + '\t' + '1/2c,3c' + '\t' + c
        elif (stsum == 8) or (stsum == 9):
            print f + '\t' + '1/2a,3a' + '\t' + c
        elif (stsum == 2) or (stsum == 3) or (stsum == 6) or (stsum == 7):
            print f + '\t' + '4b,4d,4e' + '\t' + c
        elif (stsum > 9) and (stsum < 16):
            print f + '\t' + '4b,4d,4e' + '\t' + c
        elif stsum == 1:
            print f + '\t' + '?4a,4c' + '\t' + c
        else:
            print f + '\t' + '-' + '\t' + c
            sys.stderr.write('ERROR: No amplicons found - check the submitted sequence is L.monocytogenes\n')

progexit(0)
