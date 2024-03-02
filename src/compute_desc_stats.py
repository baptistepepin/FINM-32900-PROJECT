import pandas as pd
import numpy as np
from pathlib import Path
import config



# read the .parquet file in the data directory
def read_data(file_name, data_dir=config.DATA_DIR):
    """
    Read the .parquet file in the data directory
    """
    file_path = Path(data_dir) / "pulled" / f"{file_name}.parquet"
    if file_path.exists():
        df = pd.read_parquet(file_path)
    else:
        raise FileNotFoundError(f"{file_path} not found")
    return df


# Compute the descriptive statistics
def compute_desc_stats(df):
    """
    Compute the descriptive statistics
    """
    lending_indicators = ['short interest ratio', 'loan supply ratio', 'loan utilisation ratio', 'loan fee']
    esg = ['severity', 'novelty', 'reach', 'environment', 'social', 'governance']

    # For i in esg, save each desc stats table to a .parquet file in the data directory
    for i in esg:
        file_path = Path(config.DATA_DIR) / "pulled" / f"{i}.parquet"
        df.groupby(i)[lending_indicators].describe().T.to_parquet(file_path)

    return df

if __name__ == '__main__':
    # read the .parquet file in the data directory
    df = read_data("merged_data")

    # Compute the descriptive statistics and store them in the data directory as .csv files
    _ = compute_desc_stats(df)