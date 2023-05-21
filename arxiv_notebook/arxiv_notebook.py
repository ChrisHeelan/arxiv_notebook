import os
from typing import Optional, Sequence, Union
import subprocess
import nbformat
from nbconvert.exporters import LatexExporter
from nbconvert.preprocessors import Preprocessor
from arxiv_notebook.style import ARXIV_STYLE


def create_latex_insert(
    title: str,
    date: Optional[Union[bool, str]] = True,
    authors: Optional[Sequence[dict]] = None,
    under_title: Optional[str] = None,
    header_right: Optional[str] = None,
    header_center: Optional[str] = None,
    abstract: Optional[str] = None,
) -> str:
    """
    Creates a LaTeX insert for arXiv-style document headers.

    Args:
        title (str): The title of the notebook.
        date (str or bool, optional): The date of the notebook. It can be a string or set to True to use the current
        date. Defaults to True.
        authors (list of dicts, optional): The list of authors of the notebook. Each author is represented as
            a dictionary with keys 'name', 'first_line', 'second_line', and 'email'. All keys are optional. Defaults
            to None.
        under_title (str, optional): The subheading under the title. Defaults to None.
        header_right (str, optional): The text to be displayed on the right side of the header. Defaults to None.
        header_center (str, optional): The text to be displayed in the center of the header. Defaults to None.
        abstract (str, optional): The abstract of the notebook. Defaults to None.

    Returns:
        str: The generated LaTeX insert for the document headers.
    """

    header = r"\usepackage{arxiv}" + "\n\n"
    header += r"\title{" + title + "}\n\n"

    if isinstance(date, str):
        header += r"\date{" + date + "}\n\n"

    elif date is None or date is False:
        header += r"\date{}\n\n"

    if authors is not None:
        authors_str = r"\author{" + "\n"

        for author_num, author in enumerate(authors):
            if "name" in author.keys():
                authors_str += "    " + author["name"] + r"\\" + "\n"

            if "first_line" in author.keys():
                authors_str += "    " + author["first_line"] + r"\\" + "\n"

            if "second_line" in author.keys():
                authors_str += "    " + author["second_line"] + r"\\" + "\n"

            if "email" in author.keys():
                if author_num == len(authors) - 1:
                    authors_str += r"    \texttt{" + author["email"] + r"}" + "\n"

                else:
                    authors_str += r"    \texttt{" + author["email"] + r"}\\" + "\n"

            if author_num < len(authors) - 1:
                authors_str += r"    \And" + "\n"

        authors_str += "}\n\n"

        header += authors_str

    if under_title is None:
        header += r"\renewcommand{\undertitle}{}" + "\n"

    else:
        header += r"\renewcommand{\undertitle}{" + under_title + "}\n"

    if header_right is not None:
        header += r"\renewcommand{\headeright}{" + header_right + "}\n"

    if header_center is not None:
        header += r"\renewcommand{\shorttitle}{" + header_center + "}\n\n"

    header += r"\begin{document}" + "\n    " + r"\maketitle" + "\n\n"

    if abstract is not None:
        header += r"    \begin{abstract}" + "\n"
        header += f"    {abstract}\n"
        header += r"    \end{abstract}" + "\n"

    return header


def notebook_to_arxiv(
    notebook_path: str,
    name: str,
    title: str,
    date: Optional[Union[bool, str]] = True,
    authors: Optional[Sequence[dict]] = None,
    under_title: Optional[str] = None,
    header_right: Optional[str] = None,
    header_center: Optional[str] = None,
    abstract: Optional[str] = None,
    save_notebook: bool = False,
    verbose: bool = False,
):
    """
    Converts a Jupyter notebook to a PDF using an arXiv style based on NIPS
    2018.

    Args:
        notebook_path (str): The path to the Jupyter notebook file.
        name (str): The name of the output directory and PDF file (without the extension).
        title (str): The title of the notebook.
        date (str or bool, optional): The date of the notebook. It can be a string or set to True to use the current
        date. Defaults to True.
        authors (list of dicts, optional): The list of authors of the notebook. Each author is represented as
            a dictionary with keys 'name', 'first_line', 'second_line', and 'email'. All keys are optional. Defaults
            to None.
        under_title (str, optional): The subheading under the title. Defaults to None.
        header_right (str, optional): The text to be displayed on the right side of the header. Defaults to None.
        header_center (str, optional): The text to be displayed in the center of the header. Defaults to None.
        abstract (str, optional): The abstract of the notebook. Defaults to None.
        save_notebook (bool, optional): Whether to save the notebook before conversion. Defaults to False.
        verbose (bool, optional): Whether to display verbose output during the conversion process. Defaults to False.

    Returns:
        None: The function does not return anything.
    """

    # Build a latex insert.
    latex_insert = create_latex_insert(
        title=title,
        authors=authors,
        date=date,
        under_title=under_title,
        header_right=header_right,
        header_center=header_center,
        abstract=abstract,
    )

    if save_notebook:
        from ipylab import JupyterFrontEnd
        import time

        JupyterFrontEnd().commands.execute("docmanager:save")
        time.sleep(3)

    # Load the Jupyter notebook.
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Configure the LaTeX exporter.
    exporter = LatexExporter()

    # Perform the conversion.
    (body, resources) = exporter.from_notebook_node(nb)

    # Remove previous calls to the geometry package and remove any lines that used it.
    body = body.replace(r"\usepackage{geometry}", r"%\usepackage{geometry}")
    body = body.replace(r"\geometry{", r"%\geometry{")

    # Drop the \\maketitle line and replace the \begin{document} with the latex insert.
    body = body.replace(r"\\maketitle", "")
    body = body.replace(r"\begin{document}", latex_insert)

    # If the output directory doesn't exist, create it.
    if not os.path.isdir(name):
        os.makedirs(name)

    # Change working directory into the output_path.
    working_directory = os.getcwd()
    os.chdir(name)

    # Write the LaTeX style file.
    with open(f"arxiv.sty", "w", encoding="utf-8") as f:
        f.write(ARXIV_STYLE)

    # Write the tex file.
    tex_pathname = f"{name}.tex"
    with open(tex_pathname, "w", encoding="utf-8") as f:
        f.write(body)

    # Write the resource outputs.
    for output_key in resources["outputs"].keys():
        with open(output_key, "wb") as f:
            f.write(resources["outputs"][output_key])

    # Convert the tex file to PDF.
    output = subprocess.check_output(
        ["pdflatex", tex_pathname], stderr=subprocess.STDOUT, universal_newlines=True
    )

    if verbose:
        print(output)

    os.chdir(working_directory)
