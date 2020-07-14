
---
title: 'LisSero: *In silico* serotyping of *Listeria monocytogenes*'
tags:
  - Python
  - bioinformatics
  - public health microbiology
  - microbial genomics
  - Listeria
authors:
  - name: Jason Kwong^[Corresponding author]
    orcid: 0000-0003-0872-7098
    affiliation: "1, 2"
  - name: Josh Zhang
    affiliation: 2
  - name: Kristy A. Horan
    affiliation: 2
   - name:  William R. Pitchers
     affiliation: 2
   - name: Karolina Mercoulia
     affiliation: 2
   - name: Susan Ballard
     affiliation: 2
   - name: Anders Gonçalves da Silva
      affiliation: 2
   - name: Timothy P. Stinear
     affiliation: 3
   - name: Benjamin P. Howden
     affiliation: "2, 3"
   - name: Torsten Seemann^[Corresponding author]
     affiliation: "2, 3"
affiliations:
 - name: Austin Health
   index: 1
 - name: Microbiological Diagnostic Unit Public Health Laboratory, Department of Microbiology and Immunology, The Doherty Institute for Infection and Immunity, The University of Melbourne
   index: 2
 - name: Department of Microbiology and Immunology, The Doherty Institute for Infection and Immunity, The University of Melbourne
   index: 3
date: 13 July 2020
bibliography: paper.bib

---

# Summary

One of the corner stones of transition to genomics in public health are Bioinformatic
tools to assist in replicating wet lab processes using whole-genome sequence data. A 
number of tools have been written to carry out various bacterial sub-typing techniques, 
such as multi-locus sequence typing, and various types of phenotypic serotype inferences
(e.g., *Salmonella* serotyping, and *Neisseria gonorrhoeae* multi-antigen sequence typing). 
Here we present `LisSero`, a tool for performing *Listeria monocytogenes* *in silico* serotype
inferences based on draft assemblies obtained from whole-genome sequence data.
`LisSero` will add a valuable tool to the growing number of Bioinformatics tools
designed to provide backwards compatibility with data generated prior to the dissemination
of whole-genome sequencing technology.

# Statement of need 

`LisSero` is a Python package that automates the process of `BLASTing`
a set of contigs from a draft assembly of a *Listeria monocytogenes* genome
against a curated database of five genes. The serotype is assigned in accordance 
with the combination of identified genes [@doumithDifferentiationMajorListeria2004]. 
The five genes (NAME GENES) have been described as the minimum necessary 
to classify *L. monocytogenes* isolates into distinct serotypes of public health importance [@doumithDifferentiationMajorListeria2004].

`LisSero` was designed to provide an *in silico* replacement for the muliplex PCR
based *L monocytogenes* serotyping. We provide validation data, and demonstrate
the capability of the tool to recover the expected serotype from draft assemblies
of *L. monocytogenes*. The tool is important in providing backwards compatibility, 
allowing researchers and public health labs wishing to move to WGS the ability to 
compare their strains with previously available data. The tool is already use in routinely
in our lab, and it has already been used in a number of publications [@kwongProspectiveWholeGenomeSequencing2016, @toledoGenomicDiversityListeria2018, @bainesCompleteMicrobialGenomes2019a,
@knijnAdvancedResearchInfrastructure2020].

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Fenced code blocks are rendered with syntax highlighting:
```python
for n in range(10):
    yield f(n)
```	

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlstNDc1ODEzNDM1LC0xMzMyMzIz
NDc5LDE5NjI4NTMzNjYsNjI2MzQ5MTM0LDIxODUzMDY4N119
-->