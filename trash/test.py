from lissero.Blast import Blast
import re

run_blast = Blast()
run_blast.version()
print(run_blast.version_no)
#my_str = "blastn: 2.10.0+"
#pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
#print(pattern.findall(my_str))

