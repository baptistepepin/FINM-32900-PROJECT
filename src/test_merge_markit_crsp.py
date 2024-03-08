"""
The module `test_merge_markit_crsp.py` is designed to test the functionality and integrity of merging datasets from CRSP and Markit. 
Ensuring that the merged dataset retains structural integrity and data accuracy is crucial for subsequent financial analyses. 

The module contains the following functions:
    * test_merge_markit_crsp
    * test_merge_crsp_markit_validity
"""
import pandas as pd
import numpy as np

import pytest

import config
from load_crsp import load_CRSP
from load_markit import load_Markit
from merge_markit_crsp import merge_markit_crsp

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE

def test_merge_markit_crsp():
    """
    Tests the merge function between Markit and CRSP datasets to ensure the resulting DataFrame is correctly structured 
    and contains the expected columns and data types.
    
    The function performs the following validations:
        * Confirms the merged DataFrame is a pandas DataFrame, ensuring successful integration.
        * Verifies the presence of expected columns that include both Markit and CRSP data fields, ensuring completeness 
            of the merged data.
        * Checks the data types of each column to match predefined expectations, which is crucial for the accuracy of 
            any financial computations that follow.
    """
    df1 = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df2 = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    df = merge_markit_crsp(df2, df1, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Test if the DataFrame has the expected columns
    expected_columns = ['date', 'cusip', 'isin', 'instrumentname', 'indicativefee',
       'utilisation', 'shortloanquantity', 'quantityonloan',
       'lendablequantity', 'lenderconcentration', 'borrowerconcentration',
       'inventoryconcentration', 'marketarea', 'cusip8', 'shrout',
       'short interest ratio', 'loan supply ratio', 'loan utilisation ratio',
       'loan fee']
    assert all(col in df.columns for col in expected_columns)
    
    expected_dtypes = {
    'date': np.dtype('<M8[ns]'),
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
    'cusip8': np.dtype('O'),
    'shrout': np.dtype('float64'),
    'short interest ratio': np.dtype('float64'),
    'loan supply ratio': np.dtype('float64'),
    'loan utilisation ratio': np.dtype('float64'),
    'loan fee': np.dtype('float64')
    }
    assert dict(df.dtypes)==expected_dtypes
    pass

def test_merge_crsp_markit_validity():
    """
    Validates the data integrity and consistency of the merged dataset from CRSP and Markit, focusing on the date 
    range, DataFrame shape, presence of NaN values, and accuracy of key financial ratios.
    
    The function ensures:
        * The data covers at least from the start of 2022 to the end of 2023, verifying the dataset has the intended analysis period.
        * The shape of the DataFrame matches expected dimensions, indicating successful data integration from both sources.
        * The presence of NaN values in specific columns matches expectations, assessing data completeness and potential issues with data integrity.
        * The accuracy of mean values for specific key financial ratios. This ensures the numerical integrity of the merged dataset.
    
    """
    df1 = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df2 = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    df = merge_markit_crsp(df2, df1, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    # Check that we have the data atleast from the start of 2022 to the end of 2023
    assert df['date'].min() <= pd.to_datetime('2022-01-03')
    assert df['date'].max() >= pd.to_datetime('2023-12-29')
    
    
    # Rest of the test will be from a sampled subset of the data in the range mentioned above
    df_sampled = df[(df.date.dt.year>=2022) & (df.date.dt.year<=2023)]

    # Check the shape of the dataframe
    assert df_sampled.shape == (7205931, 19)

    # Check that there are no NaNs in the data fetched
    NaNs = {
    'date': 0,
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
    'cusip8': 0,
    'shrout': 4159509,
    'short interest ratio': 4257572,
    'loan supply ratio': 4178543,
    'loan utilisation ratio': 617373,
    'loan fee': 2358177
    }
    assert dict(df_sampled.isna().sum())==NaNs

    # Check that the mean of the shrout column is correct
    means_dict = {'short interest ratio': 2.6615720138124326,
                  'loan supply ratio': 19.417989949973727,
                  'loan utilisation ratio': 16.35466789109963, 
                  'loan fee': 0.11534523060568044
                  }

    assert dict(df_sampled[['short interest ratio','loan supply ratio','loan utilisation ratio','loan fee']].mean()) == means_dict
    pass
