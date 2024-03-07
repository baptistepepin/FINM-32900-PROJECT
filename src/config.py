"""
This module facilitates loading project configurations from .env files, providing streamlined access to paths, credentials, 
and other configuration settings necessary for the project's operation. It is intended for use as an imported module across 
various parts of the project to ensure consistent access to these configurations. If `config.py` is run on its own, it will 
create the appropriate directories.

Utilizing the python-decouple package, this module adheres to the best practices of separating configuration from code, enabling 
easy switches between different environments (e.g., development, production) by simply changing the .env file. This separation 
enhances security and flexibility, allowing for different configurations without altering the codebase.

For detailed guidance on using python-decouple and its benefits in managing project configurations, refer to its documentation 
on PyPI. https://pypi.org/project/python-decouple/
"""

from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = config('DATA_DIR', default=(BASE_DIR / 'data'), cast=Path)
OUTPUT_DIR = config('OUTPUT_DIR', default=(BASE_DIR / 'output'), cast=Path)
WRDS_USERNAME = config("WRDS_USERNAME", default="")

START_DATE = config("START_DATE", default="2022-01-01")
END_DATE = config("END_DATE", default="2024-01-01")

if __name__ == "__main__":
    
    ## If they don't exist, create the data and output directories
    (DATA_DIR / 'pulled').mkdir(parents=True, exist_ok=True)

    # Sometimes, I'll create other folders to organize the data
    # (DATA_DIR / 'intermediate').mkdir(parents=True, exist_ok=True)
    # (DATA_DIR / 'derived').mkdir(parents=True, exist_ok=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'stats').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'tables').mkdir(parents=True, exist_ok=True)
