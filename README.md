# LisSero
*In silico* serogroup prediction for *Listeria monocytogenes*

## Authors
* Jason Kwong (@kwongjc) - GitHub: [kwongj](https://github.com/kwongj)  
* Torsten Seemann (@torstenseemann) - GitHub: [tseemann](https://github.com/tseemann)  

## Dependencies
* [Python 2.x](https://www.python.org/downloads/)
* ~~[EMBOSS PrimerSearch](http://emboss.sourceforge.net/download/)~~
* [isPcr](https://users.soe.ucsc.edu/~kent/) (Optional)

The primary site for EMBOSS software was down when we last checked on 26 February 2016. 
This does not seem to be a [temporary issue](https://www.biostars.org/p/147960/).

We direct the user instead to this download page to obtain a 6.5.7 version:

[EMBOSS PrimerSearch v.6.5.7](ftp://emboss.open-bio.org/pub/EMBOSS/old/6.5.0/)

For version 6.6.0 (the very latest as far as we know), one can try this
[mirror](http://debian.rub.de/ubuntu/pool/universe/e/emboss/emboss_6.6.0.orig.tar.gz) for a linux version.

*All our tests were performed on version 6.6.0.*

## Usage
`$ LisSero.py -h`  
```usage: 
  LisSero [OPTIONS] <fasta1> <fasta2> <fasta3> ... <fastaN>

In silico serogroup prediction for L.monocytogenes
Alleles: lmo1118 (16), lmo0737 (8), ORF2819 (4), ORF2110 (2), Prs (1)

positional arguments:
  FASTA              input FASTA files eg. fasta1, fasta2, fasta3 ... fastaN

optional arguments:
  -h, --help         show this help message and exit
  --primers PRIMERS  Specify alternate/custom file with serotyping primers
  --mismatch %       allowable primer mismatch percentage
                     (default=15% ie. ~3 mismatches per 20-base primer)
  --full             prints detailed output of PCR products (default=off)
                     (not recommended for large numbers of sequences)
  --ampseq           prints sequence of PCR products with primers (default=off)
                     requires isPcr by Jim Kent
  --version          show program's version number and exit
```

## Basic syntax
**To predict serogroup:**  
`$ LisSero.py <fasta1> <fasta2> <fasta3> ... <fastaN>`  
**To save output to a file:**  
`$ LisSero.py <fasta1> <fasta2> <fasta3> ... <fastaN> > results.txt`  

**To specify alternative primers for the alleles:**  
This requires a file in the format:  
  Primer-name  [Forward-primer-sequence]  [Reverse-primer-sequence]  
`$ LisSero.py --primers [primers-file] <fasta1> <fasta2> <fasta3> ... <fastaN>`   

**To change the format of the output:**  
Default = tab-delimited output  
`$ <fastaN>    [Serogroup]    [Alleles detected]`  

To show full output of detected alleles showing amplicon detected, length of amplicon, and mismatches:  
`$ LisSero.py --full <fasta1> <fasta2> <fasta3> ... <fastaN>`  

To show sequence of detected amplicons:  
`$ LisSero.py --ampseq <fasta1> <fasta2> <fasta3> ... <fastaN>`  

**To adjust the allowable primer mismatch:**  
Specify the % mismatch acceptable for primer binding:  
`$ LisSero.py mismatch % <fasta1> <fasta2> <fasta3> ... <fastaN>`  

## *In silico* PCR serogrouping for *Listeria monocytogenes*  
LisSero is based on a method of predicting serogroup for *Listeria monocytogenes* using PCR, as described by Doumith et al (see References). It detects the presence or absence of 5 DNA regions (lmo1118, lmo0737, ORF2110, ORF2819 and prs). The patterns obtained reflect the four main serotypes (1/2a, 1/2b, 1/2c, and 4b) obtained from food and human sources.

The patterns are not based on genes involved in somatic (O) or flagellar (H) biosynthesis, and are not specific to just one serotype, but rather to a group of serotypes.

| Serogroup     |  lmo1118  |  lmo0737  |  ORF2110  |  ORF2819  |   Prs   |  
| ------------- | --------- | --------- | --------- | --------- | ------- |  
| 1/2a, 3a      |     -     |     +     |     -     |     -     |   +     |  
| 1/2b, 3b, 7   |     -     |     -     |     -     |     +     |   +     |  
| 1/2c, 3c      |     +     |     +     |     -     |     -     |   +     |  
| 4b, 4d, 4e    |     -     |     -     |     +     |     +     |   +     |  
| *Listeria spp.* |           |           |           |           |   +     |  

If only Prs is detected, these isolates are often serotype 4a or 4c, though LisSero reports these as "no type (NT)".

##Bugs
Please submit via the GitHub issues page: [https://github.com/MDU-PHL/LisSero/issues](https://github.com/MDU-PHL/LisSero/issues)  

##Software Licence
GPLv2: [https://github.com/MDU-PHL/LisSero/blob/master/LICENSE](https://github.com/MDU-PHL/LisSero/blob/master/LICENSE)

## References
* Doumith et al. Differentiation of the major Listeria monocytogenes serovars by multiplex PCR.
_J Clin Microbiol_, 2004; __42:8__; 3819-22.
