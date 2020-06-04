"""
A sample class for LisSero
"""

import os

from loguru import logger

from .Serotype import Serotype


class Sample:
    def __init__(
        self,
        filename,
        blast,
        sero_db,
        sg_min_id,
        sg_min_cov,
    ):
        self.id = filename
        self.filename = os.path.realpath(filename)
        self.serotype = Serotype(blast, sero_db, pid=sg_min_id, cov=sg_min_cov)

    def is_fasta(self):
        pass

    def get_serotype(self):
        logger.info(f"Serotyping: {self.id}")
        self.serotype.generate_type(self.filename)

    def __str__(self):
        try:
            string = f"{self.id} " \
                     f"\tSEROTYPE: {self.serotype.report['serotype']}"
        except:
            string = ""
        return string


class Samples:

    SIMPLE_HEADER = ["ID", "SEROTYPE", "PRS", "LMO0737", "LMO1118", "ORF2110", "ORF2819", "COMMENT"]

    def __init__(
        self,
        filenames,
        blast,
        sero_db,
        sg_min_id,
        sg_min_cov,
    ):
        self.filenames = filenames
        self.blast = blast
        self.sero_db = sero_db
        self.sg_min_id = sg_min_id
        self.sg_min_cov = sg_min_cov

    def _create_sample(self):
        self.samples = []
        for f in self.filenames:
            self.samples += [
                Sample(
                    f,
                    blast=self.blast,
                    sero_db=self.sero_db,
                    sg_min_id=self.sg_min_id,
                    sg_min_cov=self.sg_min_cov,
                )
            ]

    def _run_typing(self, func):
        if func == "serotype":
            for f in self.samples:
                f.get_serotype()
        else:
            logger.critical(f"Unknown function {func}")
            raise RuntimeError

    def run_typing(self):
        self._create_sample()
        self._run_typing("serotype")

    def simple_report(self, header=True):
        print("\t".join(self.SIMPLE_HEADER))
        for sample in self.samples:
            sample_id = sample.serotype.report["id"]
            serotype = sample.serotype.report["serotype"]
            prs = sample.serotype.report["prs"]
            lmo0737 = sample.serotype.report["lmo0737"]
            lmo1118 = sample.serotype.report["lmo1118"]
            orf2110 = sample.serotype.report["orf2110"]
            orf2819 = sample.serotype.report["orf2819"]
            comment = sample.serotype.report["comment"]
            if comment is None:
                comment = ""
            print("\t".join([sample_id, serotype, prs, lmo0737, lmo1118, orf2110, orf2819, comment]))

    def __str__(self):
        return f"Typing {len(self.filenames)} samples"
