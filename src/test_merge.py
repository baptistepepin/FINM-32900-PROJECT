"""
The module `test_merge.py` is designed to test the robustness and correctness of the data merging processes 
used in a financial data analysis project. It specifically targets the integration of datasets 
from CRSP (Center for Research in Security Prices), Markit, and RepRisk, ensuring the merged 
dataset is properly structured and contains all expected information without significant data 
loss or mismatch.

The mdule contains the following functions:
    * test_merge
    * test_merge_crsp_markit_validity
"""
import pandas as pd
import numpy as np

import pytest

import config
from load_crsp import load_CRSP
from load_markit import load_Markit
from load_reprisk import load_RepRisk
from merge_markit_crsp import merge_markit_crsp
from merge_markit_crsp_reprisk import merge_data

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE

def test_merge():
    """
    Tests the merging process of datasets from CRSP, Markit, and RepRisk to ensure the final DataFrame is correctly structured.
    
    This function performs the following checks:
        * Verifies that the merged DataFrame is indeed a pandas DataFrame, confirming the successful merge of datasets.
        * Checks if the DataFrame contains all expected columns from the CRSP, Markit, and RepRisk datasets, ensuring comprehensive data integration.
        * Asserts that the data types of the columns are as expected, which is crucial for subsequent data manipulation and analysis.
    """
    df1 = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df2 = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df3 = merge_markit_crsp(df2, df1, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df4 = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df = merge_data(df3, df4, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = ['date', 'cusip', 'isin', 'instrumentname', 'indicativefee',
       'utilisation', 'shortloanquantity', 'quantityonloan',
       'lendablequantity', 'lenderconcentration', 'borrowerconcentration',
       'inventoryconcentration', 'marketarea', 'cusip8', 'shrout',
       'short interest ratio', 'loan supply ratio', 'loan utilisation ratio',
       'loan fee', 'reprisk_id', 'company_name', 'primary_isin', 'current_rri',
       'trend_rri', 'peak_rri', 'peak_rri_date', 'reprisk_rating',
       'country_sector_average', 'incident_date', 'story_id',
       'unsharp_incident', 'related_countries', 'related_countries_codes',
       'severity', 'reach', 'novelty', 'environment', 'social', 'governance']
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
    'loan fee': np.dtype('float64'),
    'reprisk_id': np.dtype('O'),
    'company_name': np.dtype('O'),
    'primary_isin': np.dtype('O'),
    'current_rri': np.dtype('float64'),
    'trend_rri': np.dtype('float64'),
    'peak_rri': np.dtype('float64'),
    'peak_rri_date': np.dtype('<M8[ns]'),
    'reprisk_rating': np.dtype('O'),
    'country_sector_average': np.dtype('float64'),
    'incident_date': np.dtype('<M8[ns]'),
    'story_id': np.dtype('float64'),
    'unsharp_incident': np.dtype('float64'),
    'related_countries': np.dtype('O'),
    'related_countries_codes': np.dtype('O'),
    'severity': np.dtype('float64'),
    'reach': np.dtype('float64'),
    'novelty': np.dtype('float64'),
    'environment': np.dtype('O'),
    'social': np.dtype('O'),
    'governance': np.dtype('O')
    }
    assert dict(df.dtypes)==expected_dtypes
    
    pass

def test_merge_crsp_markit_validity():
    """
    Validates the data integrity and consistency of the merged dataset from CRSP, Markit, and RepRisk, focusing on date range, DataFrame shape, and NaN values.
    
    The function ensures:
        * The date range of the data covers at least from the start of 2022 to the end of 2023, verifying that the dataset spans the intended analysis period.
        * The shape of the DataFrame matches the expected dimensions post-merge, indicating that data from all sources has been successfully integrated.
        * The presence of NaN values across different columns matches expected patterns, highlighting any potential issues with data completeness or integrity.
        * The accuracy of mean values for specific financial ratios, confirming the numerical integrity of the merged dataset.
    """
    df1 = load_CRSP(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df2 = load_Markit(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df3 = merge_markit_crsp(df2, df1, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df4 = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    df = merge_data(df3, df4, data_dir=DATA_DIR, from_cache=True, save_cache=True)

    # Check that we have the data atleast from the start of 2022 to the end of 2023
    assert df['date'].min() <= pd.to_datetime('2022-01-03')
    assert df['date'].max() >= pd.to_datetime('2023-12-29')

    # Rest of the test will be from a sampled subset of the data in the range mentioned above
    df_sampled = df[(df.date.dt.year>=2022) & (df.date.dt.year<=2023)]

    # Check the shape of the dataframe
    assert df_sampled.shape == (7206986, 39)

    # Check that there are no NaNs in the data fetched
    NaNs = {
    'date': 0,
    'cusip': 0,
    'isin': 0,
    'instrumentname': 0,
    'indicativefee': 2358273,
    'utilisation': 617468,
    'shortloanquantity': 1701326,
    'quantityonloan': 1701326,
    'lendablequantity': 617468,
    'lenderconcentration': 0,
    'borrowerconcentration': 0,
    'inventoryconcentration': 0,
    'marketarea': 0,
    'cusip8': 0,
    'shrout': 4159529,
    'short interest ratio': 4257592,
    'loan supply ratio': 4178656,
    'loan utilisation ratio': 617468,
    'loan fee': 2358273,
    'reprisk_id': 6371727,
    'company_name': 6371727,
    'primary_isin': 6371727,
    'current_rri': 6371727,
    'trend_rri': 6371727,
    'peak_rri': 6371727,
    'peak_rri_date': 6640744,
    'reprisk_rating': 6371727,
    'country_sector_average': 6371727,
    'incident_date': 7198297,
    'story_id': 7198297,
    'unsharp_incident': 7198297,
    'related_countries': 7198297,
    'related_countries_codes': 7199247,
    'severity': 7198297,
    'reach': 7198297,
    'novelty': 7198297,
    'environment': 7198297,
    'social': 7198297,
    'governance': 7198297
    }
    assert dict(df_sampled.isna().sum())==NaNs

    # Check that the mean of the shrout column is correct
    ratio_means = {'short interest ratio': 0.02660878599461014, 
                   'loan supply ratio': 0.19421440968469392, 
                   'loan utilisation ratio': 16.352578932434426, 
                   'loan fee': 0.1153239415143936}
    assert dict(df_sampled[['short interest ratio','loan supply ratio','loan utilisation ratio','loan fee']].mean()) == ratio_means
    pass
