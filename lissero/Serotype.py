'''
A class to generate a Serotype

All Serotyping logic stays here.
'''


class Serotype:
    '''
    Serotyping of Listeria monocytogenes samples is performed throught the
    presence abscense of five genes.

    One gene must be present to ascert that the species is indeed Listeria
    monocytogenes (Prs). If the gene is not present, then Serotyping CANNOT
    proceed.

    Serogroup 1/2a, 3a requires the additional presence of: lmo0737

    Serogroup 1/2b, 3b, 7 requires the additional presence of: ORF2819

    Serogroup 1/2c, 3c requires the additional presence of: lmo1118 & lmo0737

    Serogroup 4b, 4d, 4e requires the additional presence of: ORF2110 & ORF2819

    This creates a decision tree.

    What are the possible outputs?
        Alleles \in {'', Prs, lmo0737, lmo1118, ORF2819, ORF2110}

    if not Prs:
        stop
    elif lmo0737 and not (ORF2819 or ORF2110):
        if lmo1118:
            Serogroup 1/2c, 3c
        else:
            Serogroup 1/2a, 3a
    elif ORF2819 and not (lmo0737 or lmo1118):
        if ORF2110:
            Serogroup 4b, 4d, 4e
        else:
            Serogroup 1/2b, 3b, 7
    else:
        Nontypable
    '''
    def __init__(self):
        pass

    def generate_serotype(self):
        pass
