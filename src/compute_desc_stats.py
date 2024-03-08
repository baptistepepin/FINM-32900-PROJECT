"""
This module is designed to process financial data, specifically focusing on the analysis of lending indicators and 
ESG (Environmental, Social, and Governance) scores. It includes functionality to read data from a .parquet file, 
compute descriptive statistics for lending indicators across different ESG dimensions, and store the results in a 
specified output directory. The primary goal is to facilitate the examination of the relationship between lending 
behaviors and ESG metrics.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import config
from src import misc_tools


def read_data(file_name, data_dir=config.DATA_DIR):
    """
    Reads a .parquet file from a specified directory and returns a pandas DataFrame.
    """
    file_path = Path(data_dir) / "pulled" / f"{file_name}.parquet"
    if file_path.exists():
        df = pd.read_parquet(file_path)
    else:
        raise FileNotFoundError(f"{file_path} not found")
    return df


def compute_desc_stats(df):
    """
    Computes descriptive statistics for specified lending indicators across different ESG (Environmental, Social,
    and Governance) score categories and saves the results to .parquet files in the output directory.

    This function specifically calculates the descriptive statistics, including percentiles, for combinations
    of lending indicators and ESG scores, facilitating the analysis of their relationships.
    """
    lending_indicators = ['short interest ratio', 'loan supply ratio', 'loan utilisation ratio', 'loan fee']
    esg = ['severity', 'novelty', 'reach', 'environment', 'social', 'governance']

    for i in esg:
        for j in lending_indicators:
            file_path = Path(config.OUTPUT_DIR) / "stats" / f"{j + '_' + i}.parquet"
            df.groupby(i)[j].describe(percentiles=[.1, .25, .5, .75, .9]).to_parquet(file_path)

    return df

def compute_des_stats_change_days_ahead(df, days=7):
    """
    Computes descriptive statistics for the change in specified lending indicators across different ESG (Environmental, Social,
    and Governance) score categories and saves the results to .parquet files in the output directory. The change is calculated on a specified number of days ahead.

    This function specifically calculates the descriptive statistics, including percentiles, for combinations
    of change in lending indicators and ESG scores, facilitating the analysis of their relationships.
    """
    lending_indicators = ['short interest ratio', 'loan supply ratio', 'loan utilisation ratio', 'loan fee']
    esg = ['severity', 'novelty', 'reach', 'environment', 'social', 'governance']

    df_change = misc_tools.with_lagged_columns(
        data=df,
        columns_to_lag=lending_indicators,
        id_columns=['cusip'],
        lags=-days,
        date_col='date',
        prefix='L'
    )

    for j in lending_indicators:
        df_change[f'{j}_change'] = df_change[f'L-{days}_{j}'] - df_change[j]

    for i in esg:
        for j in lending_indicators:
            file_path = Path(config.OUTPUT_DIR) / "stats" / f"{j + '_' + i + '_change_' + str(days)}.parquet"
            df_change.groupby(i)[f'{j}_change'].describe(percentiles=[.1, .25, .5, .75, .9]).to_parquet(file_path)

    return df


if __name__ == '__main__':
    # read the .parquet file in the data directory
    df = read_data("merged_data")

    # Compute the descriptive statistics and store them in the data directory as .csv files
    _ = compute_desc_stats(df)
    _ = compute_des_stats_change_days_ahead(df, 5)  # 1 week ahead change
    _ = compute_des_stats_change_days_ahead(df, 26)  # 1 month ahead change
