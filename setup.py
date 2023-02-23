"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# Load version string from package
from lissero import __version__ as version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lissero",  # Required
    version=version,  # Required
    description="In silico serotyping of Listeria monocytogenes",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/MDU-PHL/lissero",  # Optional
    author="Jason Kwong",  # Optional
    author_email="kwongj@gmail.com",  # Optional
    maintainer="Josh Zhang",
    maintainer_email="josh.zhang@unimelb.edu.au",
    classifiers=[  # Optional
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="Listeria Bioinformatics Serotyping",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=3.6, <4",
    install_requires=[
        "biopython>=1.77",
        "click>=7.1.2",
        "loguru>=0.5.1",
        "numpy>=1.19.0",
        "py-fasta-validador>=0.6",
    ],  # Optional
    extras_require={  # Optional
        "dev": ["black", "flake8", "isort", "twine", "wheel"],
        "test": ["pytest", "pytest-cov"],
    },
    package_data={"lissero": ["db/lissero*", "db/sequences.fasta"]},  # Optional
    entry_points={
        "console_scripts": ["lissero = lissero.run_lissero:run_lissero"]
    },  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/MDU-PHL/lissero/issues",
        "Source": "https://github.com/MDU-PHL/lissero/",
    },
)
