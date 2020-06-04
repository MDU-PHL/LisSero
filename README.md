# LisSero

*In silico* serogroup typing prediction for *Listeria monocytogenes*

![PyPI](https://img.shields.io/pypi/v/lissero?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lissero?style=flat-square) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/lissero?style=flat-square)

## Authors

*   Jason Kwong (@kwongjc) - GitHub: [kwongj](https://github.com/kwongj)  
*   Josh Zhang (@abcdtree)  - GitHub: [abcdtree](https://github.com/abcdtree)
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
(see References).

It detects the presence or absence of 5 genes (lmo1118, lmo0737, ORF2110, ORF2819 and Prs).

The patterns obtained reflect the four main serotypes (1/2a, 1/2b, 1/2c, and 4b) 
obtained from food and human sources.

The patterns are not based on genes involved in somatic (O) or flagellar (H) biosynthesis, 
and are not specific to just one serotype, but rather to a group of serotypes.

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
  --logfile TEXT          Save log to a file instead of printing to stderr
  --debug
  --help    
```

## Example usage

```
lissero my_fasta.fa
```

## Example output

| ID                   | SEROTYPE   | PRS  | LMO0737 | LMO1118 | ORF2110 | ORF2819 | COMMENT |
| -------------------- | ---------- | ---- | ------- | ------- | ------- | ------- | ------- |
| /path/to/my_fasta.fa | 4b, 4d, 4e | FULL |  NONE   |  NONE   | FULL    | FULL    |         |

### Output explained

The output consist of 8 columns:

* ID: At the moment the full path to your file
* SEROTYPE: A predicted serotype if possible, otherwise `Nontypeable`
* Five columns for each of the genes with either:
    - `FULL`: for a complete match to the gene in the database (as defined by the `--min_cov` and `--min_id` flags
        which default to at least 95% coverage and percent id)
    - `NONE`: when there is no match to the database
    - `PARTIAL`: where there are matches that fall below the `--min_cov` and `--min_id` thresholds
 * COMMENTS: Which will try to explain a `Nontypeable` results. Current cases are:
    - `No Prs found`: when there is no `FULL` match to the `Prs` gene is not likely to be a *Listeria monocytogenes*
    - `Presence of all 5 genes, not a known serotype`: when all 5 genes are present
    - `No combination of fully matched genes resulted in a known serotype`: An unknown combination
    - In addition, it will say `Unusual 4b with lmo0737` when reporting `4b, 4d, 4e*` serotype

## Change Log

### Version 0.4.1
 * Implemented unit test for all possible 32 possible gene patterns
 * Implemented more verbose output with presence/absence info for each gene
 * Implemented test of FASTA file, and will exit with warning if a file does
    not appear to be a FASTA file
 * Implement test of whether an input file exists or not
 * Implemented logging using Loguru 
 * Added option to log to a file (`--logfile`; stderr remains default)
 * Logging now includes the BLAST command used
 * Removed all references in the code to Binary Typing
 * Implemented `--version` flag
 * Added some better docs

### Version 0.4.0
 * Removed support for Binary Typing
 * Consolidated repos in MDU-PHL
 * Changed executable from `run_lissero` to `lissero`

## Bugs
Please submit via the GitHub issues page: [https://github.com/MDU-PHL/LisSero/issues](https://github.com/MDU-PHL/LisSero/issues)  

## Software Licence
GPLv2: [https://github.com/MDU-PHL/LisSero/blob/master/LICENSE](https://github.com/MDU-PHL/LisSero/blob/master/LICENSE)

## References
*   Doumith et al. Differentiation of the major *Listeria monocytogenes* serovars by multiplex PCR. *J Clin Microbiol*, 2004; *42:8*; 3819-22.

