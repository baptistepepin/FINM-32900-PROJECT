"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""
import sys
sys.path.insert(1, './src/')


import config
from pathlib import Path
from doit.tools import run_once


OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def task_create_dirs():
    """Create the directories for the project."""
    return {
        "actions": [
            f"mkdir -p {DATA_DIR / 'pulled'}",
            f"mkdir -p {OUTPUT_DIR}",
            f"mkdir -p {OUTPUT_DIR / 'stats'}",
            f"mkdir -p {OUTPUT_DIR / 'tables'}",
        ],
    }


def task_pull_crsp():
    '''
    Pull data from CRSP and save it to a parquet file in the data/pulled directory
    '''
    file_dep = ["./src/load_crsp.py"]
    file_output = ["crsp.parquet"]
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/load_crsp.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_pull_markit():
    '''
    Pull data from Markit and save it to a parquet file in the data/pulled directory
    '''
    file_dep = ["./src/load_markit.py"]
    file_output = ["markit.parquet"]
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/load_markit.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

def task_pull_reprisk():
    '''
    Pull data from RepRisk and save it to a parquet file in the data/pulled directory
    '''
    file_dep = ["./src/load_reprisk.py"]
    file_output = ["reprisk.parquet"]
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/load_reprisk.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

def task_merge_markit_crsp_reprisk():
    '''
    Excecute the merge_markit_crsp_reprisk.py file that will merge the data from the different sources.
    '''
    file_dep = ["./src/merge_markit_crsp_reprisk.py"]
    file_output = ["merged_data.parquet"]
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/merge_markit_crsp_reprisk.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

def task_plot_lend_ind():
    '''
    Plot apple's lending indicators and store the plot in the output directory
    '''
    file_dep = ["./src/plot_lend_ind.py"]
    file_output = ["output/Apple Inc_lend_ind.png", "output/GameStop Corp_lend_ind.png", "output/Altria Group Inc_lend_ind.png"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/plot_lend_ind.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

lending_indicators = ['short interest ratio', 'loan supply ratio', 'loan utilisation ratio', 'loan fee']
esg = ['severity', 'novelty', 'reach', 'environment', 'social', 'governance']

output_files = [f"{j + '_' + i + k}.parquet" for i in esg for j in lending_indicators for k in ['', '_change_5', '_change_26']]

def task_compute_desc_stats():
    '''
    Compute the descriptive statistics and store them in the data directory as .parquet files
    '''
    file_dep = ["./src/compute_desc_stats.py"]
    file_output = output_files
    targets = [DATA_DIR / "pulled" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/compute_desc_stats.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

def task_parquet_to_latex_table():
    '''
    Convert the .parquet files to LaTeX tables
    '''
    file_dep = ["./src/pandas_to_latex_tables.py"]
    file_output = [f"{file.replace('.parquet', '.tex')}" for file in output_files]
    targets = [OUTPUT_DIR / "tables" / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/pandas_to_latex_tables.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


# def task_convert_notebooks_to_scripts():
#     """Preps the notebooks for presentation format.
#     Execute notebooks with summary stats and plots and remove metadata.
#     """
#     build_dir = Path(OUTPUT_DIR)
#     build_dir.mkdir(parents=True, exist_ok=True)
#
#     notebooks = [
#         "Project_Notebook.ipynb",
#     ]
#     file_dep = [Path("./src") / file for file in notebooks]
#     stems = [notebook.split(".")[0] for notebook in notebooks]
#     targets = [build_dir / f"_{stem}.py" for stem in stems]
#
#     actions = [
#         # *[jupyter_execute_notebook(notebook) for notebook in notebooks_to_run],
#         # *[jupyter_to_html(notebook) for notebook in notebooks_to_run],
#         *[jupyter_clear_output(notebook) for notebook in stems],
#         *[jupyter_to_python(notebook, build_dir) for notebook in stems],
#     ]
#     return {
#         "actions": actions,
#         "targets": targets,
#         "task_dep": [],
#         "file_dep": file_dep,
#         "clean": True,
#     }
#
#
# def task_run_notebooks():
#     """Preps the notebooks for presentation format.
#     Execute notebooks with summary stats and plots and remove metadata.
#     """
#     notebooks = [
#         "Project_Notebook.ipynb",
#     ]
#     stems = [notebook.split(".")[0] for notebook in notebooks]
#
#     file_dep = [
#         # 'load_other_data.py',
#         *[Path(OUTPUT_DIR) / f"_{stem}.py" for stem in stems],
#     ]
#
#     targets = [
#         ## 01_example_notebook.ipynb output
#         OUTPUT_DIR / "sine_graph.png",
#         ## Notebooks converted to HTML
#         *[OUTPUT_DIR / f"{stem}.html" for stem in stems],
#     ]
#
#     actions = [
#         *[jupyter_execute_notebook(notebook) for notebook in stems],
#         *[jupyter_to_html(notebook) for notebook in stems],
#         *[jupyter_clear_output(notebook) for notebook in stems],
#         # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
#     ]
#     return {
#         "actions": actions,
#         "targets": targets,
#         "task_dep": [],
#         "file_dep": file_dep,
#         "clean": True,
#     }


def task_compile_latex_docs():
    """Compiling the latex report"""
    file_dep = [
        "./reports/report.tex",
    ]
    file_output = [
        "./reports/report.pdf",
    ]
    targets = [file for file in file_output]

    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/report.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/report.tex",  # Clean
            # "latexmk -CA -cd ../reports/",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }
