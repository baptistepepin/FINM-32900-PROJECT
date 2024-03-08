"""
The `merge_markit_crsp.py` module defines a function to merge Markit and CRSP datasets based on dates and CUSIP8 identifiers. 
The module contains a function that checks for a cached version of the merged data in a specified directory to improve 
efficiency and avoid repeated processing. If no cached file is found, then the function proceeds to compute four ratios 
needed for further analysis. These ratios are short interest, loan supply, loan utilisation, and loan fees. Finally, 
the merged dataset can optionally be saved to a cache file for future use, streamlining subsequent data retrieval processes. 

When integrating RepRisk data with these datasets, the recommended practice from WRDS is to use the ISIN number as the primary 
key for matching with CUSIP. However, due to frequent absences of ISIN numbers in RepRisk data, a secondary matching criterion 
based on company names is also employed to ensure comprehensive data integration.
"""
import os

import pandas as pd
import config
from pathlib import Path

from load_crsp import load_CRSP
from load_markit import load_Markit

DATA_DIR = Path(config.DATA_DIR)
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def merge_markit_crsp(markit_df, crsp_df,data_dir=DATA_DIR,save_cache=False,from_cache=True):
    """
    This function merges the Markit and CRSP dataframes on dates and CUSIP8.
    """
    flag = 1
    if from_cache:
        flag = 0
        file_path = Path(data_dir) / "pulled" / "markit_crsp_ratios.parquet"
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
        else:
            flag = 1

    if flag:
        # Merge the dataframes
        df = pd.merge(
            markit_df,
            crsp_df,
            how="left",
            left_on=["cusip8", "datadate"],
            right_on=["cusip8", "date"],
        ).drop(columns=["cusip9", "date"]).rename(columns={"datadate": "date"})

    df['short interest ratio'] = df['quantityonloan']/df['shrout'] * 100
    df['loan supply ratio'] = df['lendablequantity']/df['shrout'] * 100
    df['loan utilisation ratio'] = df['utilisation']
    df['loan fee'] = df['indicativefee']

    if save_cache:
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


if __name__ == "__main__":
    # Merge the data
    markit_df = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    crsp_df = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    _ = merge_markit_crsp(markit_df, crsp_df, data_dir=DATA_DIR, from_cache=True, save_cache=True)
