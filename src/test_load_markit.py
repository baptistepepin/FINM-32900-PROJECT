import pandas as pd
import numpy as np

import pytest

import config
from load_markit import load_Markit

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE

def test_load_markit():
    df = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)
    #
    # # Test if the DataFrame has the expected columns
    expected_columns = ['datadate', 'cusip', 'isin', 'instrumentname', 'indicativefee',
       'utilisation', 'shortloanquantity', 'quantityonloan',
       'lendablequantity', 'lenderconcentration', 'borrowerconcentration',
       'inventoryconcentration', 'marketarea', 'cusip8']
    assert all(col in df.columns for col in expected_columns)
    
    expected_dtypes = {
    'datadate': np.dtype('<M8[ns]'),
    'cusip': np.dtype('O'),
    'isin': np.dtype('O'),
    'instrumentname': np.dtype('O'),
    'indicativefee': np.dtype('float64'),
    'utilisation': np.dtype('float64'),
    'shortloanquantity': np.dtype('float64'),
    'quantityonloan': np.dtype('float64'),
    'lendablequantity': np.dtype('float64'),
    'lenderconcentration': np.dtype('float64'),
    'borrowerconcentration': np.dtype('float64'),
    'inventoryconcentration': np.dtype('float64'),
    'marketarea': np.dtype('O'),
    'cusip8': np.dtype('O')
    }
    assert dict(df.dtypes)==expected_dtypes
    
    pass

def test_load_markit_data_validity():
    df = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Check that we have the data atleast from the start of 2022 to the end of 2023
    assert df['datadate'].min() <= pd.to_datetime('2022-01-03')
    assert df['datadate'].max() >= pd.to_datetime('2023-12-29')
    #
    #
    # # Rest of the test will be from a sampled subset of the data in the range mentioned above
    df_sampled = df[(df.datadate.dt.year>=2022) & (df.datadate.dt.year<=2023)]

    # # Check the shape of the dataframe
    assert df_sampled.shape == (7205931, 14)

    # # Check the number of NaNs in the data fetched
    NaNs = {
    'datadate': 0,
    'cusip': 0,
    'isin': 0,
    'instrumentname': 0,
    'indicativefee': 2358177,
    'utilisation': 617373,
    'shortloanquantity': 1701325,
    'quantityonloan': 1701325,
    'lendablequantity': 617373,
    'lenderconcentration': 0,
    'borrowerconcentration': 0,
    'inventoryconcentration': 0,
    'marketarea': 0,
    'cusip8': 0
    }
    assert dict(df_sampled.isna().sum())==NaNs

    
    # # Check that the mean of the indicative fee, utilisation, short loan quantity, lendable quantity columns is correct
    means = {'indicativefee': 0.11534523060568044, 
             'utilisation': 16.35466789109963, 
             'shortloanquantity': 2193847.795347569, 
             'lendablequantity': 19910191.71594513
             }
    
    assert dict(df_sampled[['indicativefee','utilisation','shortloanquantity','lendablequantity']].mean()) == means
    pass
