import pandas as pd
import numpy as np

import pytest

import config
from load_crsp import load_CRSP

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def test_load_crsp():
    df = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)
    #
    # # Test if the DataFrame has the expected columns
    expected_columns = ['cusip9', 'date', 'cusip8','shrout']
    assert all(col in df.columns for col in expected_columns)
    
    expected_dtypes = {
    'cusip9': np.dtype('O'),
    'date': np.dtype('<M8[ns]'),
    'cusip8': np.dtype('O'),
    'shrout': np.dtype('float64')
    }
    assert dict(df.dtypes)==expected_dtypes
    
    pass

def test_load_crsp_data_validity():
    df = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Check that we have the data atleast from the start of 2022 to the end of 2023
    assert df['date'].min() <= pd.to_datetime('2022-01-03')
    assert df['date'].max() >= pd.to_datetime('2023-12-29')
    #
    #
    # # Rest of the test will be from a sampled subset of the data in the range mentioned above
    df_sampled = df[(df.date.dt.year>=2022) & (df.date.dt.year<=2023)]

    # # Check that there are no NaNs in the data fetched
    assert df_sampled.isna().sum().sum()==0

    # # Check the shape of the dataframe
    assert df_sampled.shape == (6873181, 4)

    # # Check that the mean of the shrout column is correct
    assert df_sampled['shrout'].mean() == 100221826.06263389
    pass
