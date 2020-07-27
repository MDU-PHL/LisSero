---
title: 'LisSero: In Silico serogroup typing prediction for Listeria monocytogenes'
tags:
  - Python
  - bioinformatics
  - microbial genomics
  - in silico 
  - serogroup typing
authors:
  - name: Jason Kwong
    orcid: 
    affiliation: 1
  - name: Torsten Seemann
    affiliation: 1
  - name: Jianshu Zhang
    affiliation: 1
  - name: Anders Goncalves da Silva
    affiliation: 1
affiliations:
 - name: Microbiological Diagnostic Unit Public Health Laboratory, Department of Microbiology and Immunology, Peter Doherty Institute for Infection and Immunity, The University of Melbourne
   index: 1
 - name: Institution 2
   index: 2
date: 27 July 2020
bibliography: paper.bib
---

# Summary

Listeria monocytogenes are ubiquitous bacteria, commonly found in food and the environment, causing disease in humans, domestic and wild animals (Ragon et al., 2008). Infection is generally via the consumption of contaminated food or water with pregnant women, the elderly and immuno-suppressed people being most at risk. Listeriosis symptoms vary and illness ranges from mild in healthy individuals, presenting as flu-like with diarrhoea to the very severe resulting in high mortality. During pregnancy, the bacterium crosses the placenta to the unborn foetus often resulting in stillbirths, septic abortions or neonatal deaths.  Listeriosis in the elderly and immuno-suppressed initially presents with flu-like symptoms however often leads to meningitis and septicaemia and sometimes death. As a result of the severity of disease, the isolation of L. monocytogenes in the laboratory from human cases and food or water is a notifiable event and to support epidemiological investigations, isolates are routinely characterised in MDU PHL.

With the introduction of whole genome sequencing (WGS), the majority of conventional subtyping tools can be replaced with in silico analysis of WGS data. 

# Statement of need 

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

Lissero was designed to be used by MDU to employ SNP-based core genome phylogeny for strain comparison as part of the National Enhanced Listeria Surveillance System (NELSS) carried out by OzFoodNet Australia with the aim of identification of genomic links between isolates from human listeriosis cases and potential food and environmental sources of Listeria to support outbreak detection and investigation.


# Citations

---
title: "Bibliography"
output: html_document
bibliography: paper.bib
---

# Acknowledgements


# References

@article{doumith_differentiation_2004,
  title = {Differentiation of the {Major} {Listeria} monocytogenes {Serovars} by {Multiplex} {PCR}},
  volume = {42},
  issn = {0095-1137},
  url = {http://jcm.asm.org/cgi/doi/10.1128/JCM.42.8.3819-3822.2004},
  doi = {10.1128/JCM.42.8.3819-3822.2004},
  language = {en},
  number = {8},
  urldate = {2020-07-27},
  journal = {Journal of Clinical Microbiology},
  author = {Doumith, M. and Buchrieser, C. and Glaser, P. and Jacquet, C. and Martin, P.},
  month = aug,
  year = {2004},
  pages = {3819--3822}
}