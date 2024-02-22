"""
This module pulls and saves data from Markit.
"""

from datetime import datetime
from pathlib import Path

import pandas as pd
import wrds

from src import config

DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def pull_Markit(
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    # TODO: Add docstring
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    db = wrds.Connection(wrds_username=wrds_username)

    df = pd.DataFrame()
    # loop through the years to extract identifiers
    for yr in range(start_date.year, end_date.year + 1, 1):
        print(f"Pulling data for year {yr}")
        _df = db.raw_sql(f"""SELECT datadate, dxlid, isin, sedol, cusip, instrumentname
        FROM markit_msf_analytics_eqty_amer.amereqty{yr}""", date_cols=['datadate'])

        # append new year's records to the existing dataframe
        df = pd.concat([df, _df])

    db.close()

    return df


def load_Markit(
        data_dir=DATA_DIR,
        from_cache=True,
        save_cache=False,
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    # TODO: Add docstring
    """
    if from_cache:
        file_path = Path(data_dir) / "pulled" / "markit.parquet"
        MarkitSecurities_american_equities = pd.read_parquet(file_path)

    else:
        MarkitSecurities_american_equities = pull_Markit(start_date=START_DATE, end_date=END_DATE,
                                                         wrds_username=WRDS_USERNAME)

        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            MarkitSecurities_american_equities.to_parquet(file_dir / 'markit.parquet')

    return MarkitSecurities_american_equities


if __name__ == "__main__":
    # Pull and save cache of Markit data
    _ = load_Markit(data_dir=DATA_DIR, from_cache=True, save_cache=True, start_date=START_DATE, end_date=END_DATE,
                    wrds_username=WRDS_USERNAME)
