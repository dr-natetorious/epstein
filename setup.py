"""Setup configuration for the Epstein Document Exploration Toolkit."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="epstein",
    version="0.1.0",
    author="dr-natetorious",
    description="A comprehensive toolkit for exploring email dumps and image datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dr-natetorious/epstein",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "jupyter>=1.0.0",
        "notebook>=7.0.0",
        "ipywidgets>=8.0.0",
        "python-dateutil>=2.8.0",
        "tqdm>=4.65.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="email parser image analyzer forensics data exploration",
)
