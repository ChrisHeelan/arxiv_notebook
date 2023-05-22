# arxiv_notebook

This Python module provides a convenient way to convert Jupyter notebooks to PDFs using an arXiv style based on NIPS 2018. It allows you to generate PDFs with a professional-looking format.

This module uses the [arxiv-style](https://github.com/kourgeorge/arxiv-style) style from [kourgeorge](https://github.com/kourgeorge).

## Installation

To use this package, you need to have Python 3 installed on your system. You can install the package using `pip` by running the following command:

```
pip install https://github.com/ChrisHeelan/arxiv_notebook/archive/main.zip
```

## Usage

For a complete example of the package, see the [example notebook](https://github.com/ChrisHeelan/arxiv_notebook/blob/main/example/example.ipynb) and [resulting PDF](https://github.com/ChrisHeelan/arxiv_notebook/blob/main/example/output/output.pdf).

The package provides a function called `notebook_to_arxiv` that performs the conversion from a Jupyter notebook to a PDF using the arXiv style. Here is an example of how to use it:

```python
from arxiv_notebook import notebook_to_arxiv

notebook_path = '/path/to/notebook.ipynb'
name = 'output'
title = 'My Notebook Title'
date = '2023-05-21'
authors = [
    {'name': 'Author 1', 'email': 'author1@example.com'},
    {'name': 'Author 2', 'email': 'author2@example.com'},
]
under_title = 'Subheading'
header_right = 'Header Right'
header_center = 'Header Center'
abstract = 'This is the abstract of my notebook.'

notebook_to_arxiv(
    notebook_path=notebook_path,
    name=name,
    title=title,
    date=date,
    authors=authors,
    under_title=under_title,
    header_right=header_right,
    header_center=header_center,
    abstract=abstract,
    save_notebook=True,
    verbose=True
)
```

In the above example, you need to provide the following parameters:

- `notebook_path` (str): The path to the Jupyter notebook file.
- `name` (str): The name of the output directory and PDF file (without the extension).
- `title` (str): The title of the notebook.
- `date` (str or bool, optional): The date of the notebook. It can be a string or set to True to use the current date. Defaults to True.
- `authors` (list of dicts, optional): The list of authors of the notebook. Each author is represented as a dictionary with keys 'name', 'first_line', 'second_line', and 'email'. All keys are optional. Defaults to None.
- `under_title` (str, optional): The subheading under the title. By default, it is set to `None`.
- `header_right` (str, optional): The text to be displayed on the right side of the header. By default, it is set to `None`.
- `header_center` (str, optional): The text to be displayed in the center of the header. By default, it is set to `None`.
- `abstract` (str, optional): The abstract of the notebook. By default, it is set to `None`.
- `save_notebook` (bool, optional): Whether to save the notebook before conversion. By default, it is set to `False`.
- `output_path` (str, optional): Where to write outputs. Defaults to "output".
- `config`: (traitlets.config.Config, optional): User configuration instance passed to nbconvert.exportersLatexExporter. See nbconvert documentation: https://nbconvert.readthedocs.io/en/latest/nbconvert_library.html#Using-different-preprocessors.
- `verbose` (bool, optional): Whether to display verbose output during the conversion process. By default, it is set to `False`.

After running the `notebook_to_arxiv` function, a directory with the specified `name` will be created, containing the generated PDF file and other necessary files.

Please note that this package requires `pdflatex` to be installed on your system for converting the generated LaTeX file to a PDF. This can be accomplished on Ubuntu running the following command.

```bash
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
```
