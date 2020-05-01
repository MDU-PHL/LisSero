# LisSero

*In silico* serogroup and binary typing prediction for *Listeria monocytogenes*

## Authors

*   Jason Kwong (@kwongjc) - GitHub: [kwongj](https://github.com/kwongj)  
*   Torsten Seemann (@torstenseemann) - GitHub: [tseemann](https://github.com/tseemann)

## Maintainers

* MDU PHL - Josh Zhang, Kristy Horan, and Anders Gonçalves da Silva

## Dependencies

*   [Python 3.6+](https://www.python.org/downloads/)
*   [BLAST 2.10.0](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

## Installation

    pip3 install lissero


### Installing BLAST 2.10.0

**Brew**:

    brew install blast

**Conda**:

    conda install -c bioconda blast 

## *In silico* serogrouping for *Listeria monocytogenes*

LisSero is based on a method of predicting serogroup for
*Listeria monocytogenes* using PCR, as described by Doumith *et al*
(see References). It detects the presence or absence of 5 DNA regions
(lmo1118, lmo0737, ORF2110, ORF2819 and Prs). The patterns obtained reflect the
four main serotypes (1/2a, 1/2b, 1/2c, and 4b) obtained from food and
human sources.

The patterns are not based on genes involved in somatic (O) or flagellar (H) biosynthesis, and are not specific to just one serotype, but rather to a group of serotypes.

| Serogroup       | lmo1118  | lmo0737   | ORF2110   | ORF2819   | Prs     |
| --------------- | -------- | --------- | --------- | --------- | ------- |
| 1/2a, 3a        |     -    |     +     |     -     |     -     |   +     |
| 1/2b, 3b, 7     |     -    |     -     |     -     |     +     |   +     |
| 1/2c, 3c        |     +    |     +     |     -     |     -     |   +     |
| 4b, 4d, 4e      |     -    |     -     |     +     |     +     |   +     |
| 4b, 4d, 4e*     |     -    |     +     |     +     |     +     |   +     |
| *Listeria spp.* |          |           |           |           |   +     |

If only Prs is detected, these isolates are often serotype 4a or 4c, though
LisSero reports these as "Nontypable".

## Usage

```
$ lissero --help

Usage: lissero [OPTIONS] FASTA...

  In silico serogroup prediction for L. monocytogenes. Alleles: lmo1118,
  lmo0737, ORF2819, ORF2110, Prs

  References:

  * Doumith et al. Differentiation of the major Listeria monocytogenes
  serovars by multiplex PCR. J Clin Microbiol, 2004; 42:8; 3819-22

Options:
  -s, --serotype_db TEXT
  --min_id FLOAT          Minimum percent identity to accept a match. [0-100]
                          [default: 95.0]

  --min_cov FLOAT         Minimum coverage of the gene to accept a match.
                          [0-100]  [default: 95.0]

  --debug
  --help    
```

## Bugs
Please submit via the GitHub issues page: [https://github.com/MDU-PHL/LisSero/issues](https://github.com/MDU-PHL/LisSero/issues)  

## Software Licence
GPLv2: [https://github.com/MDU-PHL/LisSero/blob/master/LICENSE](https://github.com/MDU-PHL/LisSero/blob/master/LICENSE)

## References
*   Doumith et al. Differentiation of the major *Listeria monocytogenes* serovars by multiplex PCR. *J Clin Microbiol*, 2004; *42:8*; 3819-22.

