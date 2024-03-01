"""
This module pulls and saves data on fundamentals from CRSP.
It pulls the number of shares outstanding that we will need later for calculating our ratios.

The CUSIP9 retrieved from the stksecurityinfohist table is used to link CRSP and Markit data according to this page
https://wrds-www.wharton.upenn.edu/pages/wrds-research/database-linking-matrix/linking-markit-with-crsp-2/#connecting-with-crsp
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

    We need the 9 digits CUSIP to be able to link CRSP and Markit data, this CUSIP9 is available in the stksecurityinfohist table.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    query = f"""
    SELECT 
        dsf.date,
        dsf.cusip AS cusip8,
        ssih.cusip9,
        dsf.shrout
    FROM crspq.dsf AS dsf
    LEFT JOIN ( SELECT permno, permco, cusip, cusip9 FROM crspq.stksecurityinfohist
            WHERE cusip9 IS NOT NULL
            GROUP BY permno, permco, cusip, cusip9) AS ssih
        ON dsf.permno = ssih.permno AND dsf.permco = ssih.permco AND dsf.cusip = ssih.cusip
    WHERE 
        dsf.date BETWEEN '{start_date}' AND '{end_date}'
    """
    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(
        query, date_cols=["date"]
    )
    db.close()

    df["shrout"] = df["shrout"] * 1000

    # We resample daily and ffill to have a match with the Markit data
    df = df.set_index("date").sort_index().groupby("cusip9").resample("D").ffill().drop(columns=["cusip9"]).reset_index()

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
    flag = 1
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
