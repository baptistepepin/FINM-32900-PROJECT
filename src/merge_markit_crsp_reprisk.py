import os

import pandas as pd
import config
from pathlib import Path

from load_crsp import load_CRSP
from load_markit import load_Markit
from load_reprisk import load_RepRisk
from merge_markit_crsp import merge_markit_crsp

DATA_DIR = Path(config.DATA_DIR)
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def merge_data(
    markit_crsp_df,
    reprisk_df,
    data_dir=DATA_DIR,
    from_cache=True,
    save_cache=False,
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

        # Merge the two dataframes
        df = pd.merge(
            markit_crsp_df,
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

    markit_df = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    crsp_df = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    reprisk_df = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    markit_crsp_df = merge_markit_crsp(markit_df, crsp_df, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    _ = merge_data(markit_crsp_df, reprisk_df, data_dir=DATA_DIR, from_cache=True, save_cache=True)

