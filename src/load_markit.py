"""
The `load_markit.py` module has been designed to pull and save data from Markit Library. 

The module contains the following functions:
    * pull_Markit - Pulls data from the Markit Library.
    * load_Markit - Loads data from the Markit Library.

From the Markit library, we will download all the data containing information about American equities from the following table:
    * amereqty

After pulling all the data, we will append the data from each year into a single dataframe.
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


def pull_Markit(
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    The `pull_Markit` function has been designed to pull data from the Markit Library using the `wrds` package.
    This function will pull data from the `amereqty` table, which contains information about American equities for a particular year. After the 
    data has been pulled, the function will append the data from each year into a single dataframe.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    db = wrds.Connection(wrds_username=wrds_username)

    df = pd.DataFrame()
    # loop through the years to extract identifiers
    for yr in range(start_date.year, end_date.year + 1, 1):
        print(f"Pulling data for year {yr}")

        query = f"""
            SELECT 
                msf.datadate,
                msf.cusip,
                msf.isin,
                msf.instrumentname,
                msf.indicativefee,
                msf.utilisation,
                msf.shortloanquantity,
                msf.quantityonloan,
                msf.lendablequantity,
                msf.lenderconcentration,
                msf.borrowerconcentration,
                msf.inventoryconcentration
            FROM markit_msf_analytics_eqty_amer.amereqty{yr} AS msf
            """

        _df = db.raw_sql(query, date_cols=['datadate'])

        # append new year's records to the existing dataframe
        df = pd.concat([df, _df])

    df['cusip'].fillna(df['isin'].str[2:11])

    # Drop lines with missing CUSIP
    df = df.dropna(subset=['cusip'])

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
    The `load_Markit` function has been designed to load data from the Markit Library. 
    This function utilizes a caching mechanism that checks if the data for the specified date range has already been pulled and saved locally
    as a Parquet file. This approach reduces unnecessary data retrieval operations, saving time and computational resources.

    The function returns a DataFrame containing the Markit data for the specified date range.
    """
    flag = 1
    if from_cache:
        flag = 0
        file_path = Path(data_dir) / "pulled" / "markit.parquet"
        if os.path.exists(file_path):
            MarkitSecurities_american_equities = pd.read_parquet(file_path)
        else:
            flag = 1
    
    if flag:
        MarkitSecurities_american_equities = pull_Markit(start_date=start_date, end_date=end_date,
                                                         wrds_username=wrds_username)

        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            MarkitSecurities_american_equities.to_parquet(file_dir / 'markit.parquet')

    return MarkitSecurities_american_equities


if __name__ == "__main__":
    # Pull and save cache of Markit data
    _ = load_Markit(data_dir=DATA_DIR, from_cache=True, save_cache=True, start_date=START_DATE, end_date=END_DATE,
                    wrds_username=WRDS_USERNAME)
