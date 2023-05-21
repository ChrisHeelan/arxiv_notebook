from setuptools import setup, find_packages
import pathlib


# Get the README.md for long description.
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

INSTALL_REQUIRES = ["nbformat", "nbconvert", "ipylab", "pytest", "pytest-cov"]

setup(
    name="arxiv_notebook",
    version="0.1.0",
    description="Convert Jupyter notebooks to NIPS 2018 style PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChrisHeelan/arxiv_notebook",
    author="Chris Heelan",
    author_email="heelancd@gmail.com",
    packages=find_packages(),
    python_requires=">=3.9, <4",
    install_requires=INSTALL_REQUIRES,
)
