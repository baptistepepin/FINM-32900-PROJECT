r"""
You can test out the latex code in the following minimal working
example document:

\documentclass{article}
\usepackage{booktabs}
\begin{document}
First document. This is a simple example, with no 
extra parameters or packages included.

\begin{table}
\centering
YOUR LATEX TABLE CODE HERE
%\input{example_table.tex}
\end{table}
\end{document}

"""
import os

import pandas as pd
import numpy as np
np.random.seed(100)

import config
from pathlib import Path
DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)


## Suppress scientific notation and limit to 3 decimal places
# Sets display, but doesn't affect formatting to LaTeX
pd.set_option('display.float_format', lambda x: '%.4f' % x)
# Sets format for printing to LaTeX
float_format_func = lambda x: '{:.4f}'.format(x)


def parquet_to_latex_table(output_dir=OUTPUT_DIR):
    """
    Read the .parquet file in the data directory and convert to LaTeX table
    """
    file_names = []
    for root, dirs, files in os.walk(OUTPUT_DIR / "stats"):
        for file in files:
            file_names.append(file)

    for file_name in file_names:
        df = pd.read_parquet(OUTPUT_DIR / "stats" / file_name)

        latex_table_string = df.to_latex(float_format=float_format_func).replace("%", "\%")
        path = output_dir / "tables" / f'{file_name.replace(" ","_")}.tex'
        with open(path, "w") as text_file:
            text_file.write(latex_table_string)


if __name__ == '__main__':
    # Compute the descriptive statistics and store them in the data directory as .csv files
    parquet_to_latex_table(output_dir=OUTPUT_DIR)
