import os
from arxiv_notebook import notebook_to_arxiv
import nbformat
import tempfile


def test_notebook_to_arxiv(tmpdir):
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Test case 1: Minimal inputs
    notebook_path = f"{temp_path}/test_notebook.ipynb"
    name = 'output'
    output_path = f"{temp_path}/output"
    title = "Test Title"
    expected_tex_path = os.path.join(output_path, f"{name}.tex")
    expected_pdf_path = os.path.join(output_path, f"{name}.pdf")

    # Create a minimal notebook file
    nb = nbformat.v4.new_notebook()
    nbformat.write(nb, notebook_path)

    # Call the function
    notebook_to_arxiv(notebook_path, name, title, output_path=output_path)

    # Check the existence of the output files
    assert os.path.isfile(expected_tex_path)
    assert os.path.isfile(expected_pdf_path)

    # Test case 2: Full inputs with verbose output
    notebook_path = f"{temp_path}/test_notebook2.ipynb"
    name = f"{temp_path}/output2"

    notebook_path = f"{temp_path}/test_notebook2.ipynb"
    name = 'output2'
    output_path = f"{temp_path}/output"

    title = "Test Title"
    date = "2023-05-21"
    authors = [
        {
            "name": "John Doe",
            "first_line": "Department of Computer Science",
            "second_line": "University of Example",
            "email": "johndoe@example.com",
        }
    ]
    under_title = "Test Subheading"
    header_right = "Right Text"
    header_center = "Center Text"
    abstract = "This is an abstract."
    expected_tex_path = os.path.join(output_path, f"{name}.tex")
    expected_pdf_path = os.path.join(output_path, f"{name}.pdf")

    # Create a minimal notebook file
    nb = nbformat.v4.new_notebook()
    nbformat.write(nb, notebook_path)

    # Call the function
    notebook_to_arxiv(
        notebook_path,
        name,
        title,
        date,
        authors,
        under_title,
        header_right,
        header_center,
        abstract,
        output_path=output_path,
        verbose=True,
    )

    # Check the existence of the output files
    assert os.path.isfile(expected_tex_path)
    assert os.path.isfile(expected_pdf_path)

    temp_dir.cleanup()
