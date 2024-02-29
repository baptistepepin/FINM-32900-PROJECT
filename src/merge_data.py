"""
This module merges the different data sources.

The best way to do so is by using a match on CUSIP for CRSP and Markit in order to retrieve the number of shares outstanding.

For RepRisk, WRDS advises to use the ISIN number to match on CUSIP.
A lot of ISIN numbers are missing in the RepRisk data, so a match on company name is also necessary.
"""
import os

import pandas as pd
import config
from pathlib import Path

from load_crsp import load_CRSP
from load_markit import load_Markit
from load_reprisk import load_RepRisk

DATA_DIR = Path(config.DATA_DIR)
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def merge_markit_crsp(markit_df, crsp_df,data_dir=DATA_DIR):
    """
    This function merges the Markit and CRSP dataframes on dates and CUSIP9.
    """
    # Merge the dataframes
    df = pd.merge(
        markit_df,
        crsp_df,
        how="left",
        left_on=["cusip", "datadate"],
        right_on=["cusip9", "date"],
    ).drop(columns=["cusip9", "date"]).rename(columns={"datadate": "date"})

    df['short interest ratio'] = df['quantityonloan']/df['shrout']
    df['loan supply ratio'] = df['lendablequantity']/df['shrout']
    df['loan utilisation ratio'] = df['utilisation']
    df['loan fee'] = df['indicativefee']

    file_dir = Path(data_dir) / "pulled"
    df.to_parquet(file_dir / 'markit_crsp_ratios.parquet')

    return df


# def merge_reprisk_crsp(reprisk_df, crsp_df):
#     """
#     This function merges the RepRisk and CRSP dataframes
#     See https://wrds-www.wharton.upenn.edu/pages/wrds-research/database-linking-matrix/linking-reprisk-with-crsp/
#     """
#     reprisk_df['cusip_reprisk'] = reprisk_df['primary_isin'].str[2:10]
#
#     df = pd.merge(
#         reprisk_df,
#         crsp_df,
#         how="left",
#         left_on=["cusip_reprisk", "date"],
#         right_on=["cusip", "date"],
#     ).rename(columns={"cusip": "cusip_crsp", "date_x": "date_reprisk", "date_y": "date_crsp"})
#
#     return df


def merge_data(
    markit_df,
    crsp_df,
    reprisk_df,
    data_dir=DATA_DIR,
    from_cache=True,
    save_cache=False,
    start=START_DATE,
    end=END_DATE,
):
    """

    """

    flag = 1
    if from_cache:
        flag = 0
        file_path = Path(data_dir) / "pulled" / "merged_data.parquet"
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
        else:
            flag = 1

    if flag:
        markit_crsp = merge_markit_crsp(markit_df, crsp_df)

        # Merge the two dataframes
        df = pd.merge(
            markit_crsp,
            reprisk_df,
            how="left",
            on=["cusip", "date"]
        )

        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            df.to_parquet(file_dir / 'merged_data.parquet')

    return df


if __name__ == "__main__":
    # Merge the data
    markit_df = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    crsp_df = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    reprisk_df = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    _ = merge_data(markit_df, crsp_df, reprisk_df, start=START_DATE, end=END_DATE, data_dir=DATA_DIR, from_cache=False, save_cache=True)
