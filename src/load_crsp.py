"""
This module pulls and saves data on fundamentals from CRSP.
It pulls the number of shares outstanding that we will need later for calculating our ratios.
"""

from datetime import datetime
from pathlib import Path
import os
import pandas as pd
import wrds

import config

DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def pull_CRSP(
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    # TODO: Update docstring
    Pulls CRSP stock data from a specified start date to end date.

    SQL query to pull data
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    query = f"""
    SELECT 
        date, permno, permco, cusip, shrout
    FROM crspq.dsf AS dsf
    WHERE 
        date BETWEEN '{start_date}' AND '{end_date}'
    """
    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(
        query, date_cols=["date"]
    )
    db.close()

    df["shrout"] = df["shrout"] * 1000

    return df


def load_CRSP(
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
        flag = 0
        file_path = Path(data_dir) / "pulled" / "crsp.parquet"
        if os.path.exists(file_path):
            CRSP_daily_stock = pd.read_parquet(file_path)
        else:
            flag=1
    
    if flag:
        CRSP_daily_stock = pull_CRSP(start_date=start_date, end_date=end_date, wrds_username=wrds_username)

        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            CRSP_daily_stock.to_parquet(file_dir / 'crsp.parquet')

    return CRSP_daily_stock


if __name__ == "__main__":
    # Pull and save cache of CRSP data
    _ = load_CRSP(data_dir=DATA_DIR, from_cache=True, save_cache=True, start_date=START_DATE, end_date=END_DATE,
                  wrds_username=WRDS_USERNAME)
