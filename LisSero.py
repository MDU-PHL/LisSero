#!/usr/bin/env python
# Script by Jason Kwong
# In silico serotyping for L.monocytogenes

# Usage
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
	formatter_class=RawTextHelpFormatter,
	description='In silico serogroup prediction for L.monocytogenes\n\nAlleles: lmo1118 (16), lmo0737 (8), ORF2819 (4), ORF2110 (2), Prs (1)\n'
		'Ref: Doumith et al. Differentiation of the major Listeria monocytogenes serovars by multiplex PCR.\n'
		'J Clin Microbiol, 2004; 42:8; 3819-22',
	usage='\n  %(prog)s [OPTIONS] <fasta1> <fasta2> <fasta3> ... <fastaN>')
parser.add_argument('fasta', metavar='FASTA', nargs='+', help='input FASTA files eg. fasta1, fasta2, fasta3 ... fastaN')
parser.add_argument('--primers', metavar='PRIMERS', help='Specify alternate/custom file with serotyping primers')
parser.add_argument('--mismatch', metavar='%', default='15', help='allowable primer mismatch percentage\n' '(default=15%% ie. ~3 mismatches per 20-base primer)')
parser.add_argument('--full', action='store_true', help='prints detailed output of PCR products (default=off)\n' '(not recommended for large numbers of sequences)')
parser.add_argument('--ampseq', action='store_true', help='prints sequence of PCR products with primers (default=off)\n' 'requires isPcr by Jim Kent')
parser.add_argument('--version', action='version', version=
	'========================================\n'
	'%(prog)s v0.1\n'
	'Updated 3-Sept-2015 by Jason Kwong\n'
	'Dependencies: Python 2.x, EMBOSS PrimerSearch, isPcr\n'
	'========================================')
args = parser.parse_args()

# Modules and Functions
import sys
import os
import os.path
import subprocess
from subprocess import Popen

# Program exit
def progexit(n):
	sys.exit(n)

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
	primers = os.path.dirname(os.path.realpath(sys.argv[0])) + "/primers"

# Load dictionaries
ampsize = {16:906, 8:691, 4:471, 2:597, 1:370}		# Dictionary for expected amplicon size

serotype = {}
serotype[0] = "-"
serotype[1] = "Prs"
serotype[2] = "ORF2110"
serotype[3] = "ORF2110,Prs"
serotype[4] = "ORF2819"
serotype[5] = "ORF2819,Prs"
serotype[6] = "ORF2819,ORF2110"
serotype[7] = "ORF2819,ORF2110,Prs"
serotype[8] = "lmo0737"
serotype[9] = "lmo0737,Prs"
serotype[10] = "lmo0737,ORF2110"
serotype[11] = "lmo0737,ORF2110,Prs"
serotype[12] = "lmo0737,ORF2819"
serotype[13] = "lmo0737,ORF2819,Prs"
serotype[14] = "lmo0737,ORF2110,ORF2819"
serotype[15] = "lmo0737,ORF2110,ORF2819,Prs"
serotype[16] = "lmo1118"
serotype[17] = "lmo1118,Prs"
serotype[18] = "lmo1118,ORF2110"
serotype[19] = "lmo1118,ORF2110,Prs"
serotype[20] = "lmo1118,ORF2819"
serotype[21] = "lmo1118,ORF2819,Prs"
serotype[22] = "lmo1118,ORF2110,ORF2819"
serotype[23] = "lmo1118,ORF2110,ORF2819,Prs"
serotype[24] = "lmo1118,lmo0737"
serotype[25] = "lmo1118,lmo0737,Prs"
serotype[26] = "lmo1118,lmo0737,ORF2110"
serotype[27] = "lmo1118,lmo0737,ORF2110,Prs"
serotype[28] = "lmo1118,lmo0737,ORF2819"
serotype[29] = "lmo1118,lmo0737,ORF2819,Prs"
serotype[30] = "lmo1118,lmo0737,ORF2110,ORF2819"
serotype[31] = "lmo1118,lmo0737,ORF2110,ORF2819,Prs"


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
