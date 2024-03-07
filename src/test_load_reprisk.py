import pandas as pd
import numpy as np

import pytest

import config
from load_reprisk import load_RepRisk

DATA_DIR = config.DATA_DIR
START_DATE = config.START_DATE
END_DATE = config.END_DATE


def test_load_reprisk():
    df = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)
    #
    # # Test if the DataFrame has the expected columns
    expected_columns = ['reprisk_id', 'date', 'company_name', 'primary_isin', 'current_rri',
       'trend_rri', 'peak_rri', 'peak_rri_date', 'reprisk_rating',
       'country_sector_average', 'incident_date', 'story_id',
       'unsharp_incident', 'related_countries', 'related_countries_codes',
       'severity', 'reach', 'novelty', 'environment', 'social', 'governance',
       'cusip']
    assert all(col in df.columns for col in expected_columns)
    
    expected_dtypes = {
    'reprisk_id': np.dtype('O'),
    'date': np.dtype('<M8[ns]'),
    'company_name': np.dtype('O'),
    'primary_isin': np.dtype('O'),
    'current_rri': np.dtype('int64'),
    'trend_rri': np.dtype('int64'),
    'peak_rri': np.dtype('int64'),
    'peak_rri_date': np.dtype('<M8[ns]'),
    'reprisk_rating': np.dtype('O'),
    'country_sector_average': np.dtype('int64'),
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
    'governance': np.dtype('O'),
    'cusip': np.dtype('O')
    }
    assert dict(df.dtypes)==expected_dtypes
    
    pass

def test_load_reprisk_data_validity():
    df = load_RepRisk(start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR, from_cache=True, save_cache=True)
    
    # # Check that we have the data atleast for the year 2022 ( Reprisk does not have the data beyond this year )
    assert df['date'].min() <= pd.to_datetime('2022-01-01')
    assert df['date'].max() >= pd.to_datetime('2022-12-31')
    #
    #
    # # Rest of the test will be from a sampled subset of the data in the range mentioned above
    df_sampled = df[df.date.dt.year>=2022]

    # # Check the shape of the dataframe
    assert df_sampled.shape == (8540060, 22)

    # # Check the number of NaNs in the data fetched
    NaNs = {
    'reprisk_id': 0,
    'date': 0,
    'company_name': 0,
    'primary_isin': 0,
    'current_rri': 0,
    'trend_rri': 0,
    'peak_rri': 0,
    'peak_rri_date': 3482683,
    'reprisk_rating': 0,
    'country_sector_average': 0,
    'incident_date': 8507622,
    'story_id': 8507622,
    'unsharp_incident': 8507622,
    'related_countries': 8507622,
    'related_countries_codes': 8510279,
    'severity': 8507622,
    'reach': 8507622,
    'novelty': 8507622,
    'environment': 8507622,
    'social': 8507622,
    'governance': 8507622,
    'cusip': 0
    }
    assert dict(df_sampled.isna().sum())==NaNs

    # # Check that the mean of the indicative fee, utilisation, short loan quantity, lendable quantity columns is correct
    descriptions = """
       environment social governance
count        32438  32438      32438
unique           2      2          2
top              F      F          F
freq         21761  16325      21219
""".strip()

    assert df_sampled[['environment','social','governance']].describe().to_string().strip() == descriptions
    pass
