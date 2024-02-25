"""
This module pulls and saves data from RepRisk.
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


def pull_RepRisk(
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    # TODO: Add docstring
    """
    query = f"""
        SELECT
            reprisk_v2.v2_metrics.reprisk_id,
            reprisk_v2.v2_metrics.date,
            reprisk_v2.v2_wrds_company_id_table.company_name,
            reprisk_v2.v2_wrds_company_id_table.primary_isin,
            reprisk_v2.v2_metrics.current_rri,
            reprisk_v2.v2_metrics.trend_rri,
            reprisk_v2.v2_metrics.peak_rri,
            reprisk_v2.v2_metrics.peak_rri_date,
            reprisk_v2.v2_metrics.reprisk_rating,
            reprisk_v2.v2_metrics.country_sector_average,
            reprisk_v2.v2_risk_incidents.incident_date,
            reprisk_v2.v2_risk_incidents.story_id,
            reprisk_v2.v2_risk_incidents.unsharp_incident,
            reprisk_v2.v2_risk_incidents.related_countries,
            reprisk_v2.v2_risk_incidents.related_countries_codes,
            reprisk_v2.v2_risk_incidents.severity,
            reprisk_v2.v2_risk_incidents.reach,
            reprisk_v2.v2_risk_incidents.novelty,
            reprisk_v2.v2_risk_incidents.environment,
            reprisk_v2.v2_risk_incidents.social,
            reprisk_v2.v2_risk_incidents.governance
        
        FROM reprisk_v2.v2_metrics
        LEFT JOIN reprisk_v2.v2_wrds_company_id_table
            ON reprisk_v2.v2_metrics.reprisk_id = reprisk_v2.v2_wrds_company_id_table.reprisk_id
        LEFT JOIN reprisk_v2.v2_risk_incidents
            ON reprisk_v2.v2_metrics.reprisk_id = reprisk_v2.v2_risk_incidents.reprisk_id
                AND reprisk_v2.v2_metrics.date = reprisk_v2.v2_risk_incidents.incident_date
        
        WHERE reprisk_v2.v2_metrics.date BETWEEN
            '{start_date}'::date AND '{end_date}'::date
        """
    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(
        query, date_cols=["date", "peak_rri_date", "incident_date"]
    )
    db.close()

    return df


def load_RepRisk(
        data_dir=DATA_DIR,
        from_cache=True,
        save_cache=False,
        start_date=START_DATE,
        end_date=END_DATE,
        wrds_username=WRDS_USERNAME
):
    """
    # TODO: Add docstring
    """
    flag = 1
    if from_cache:
        flag = 0
        file_path = Path(data_dir) / "pulled" / "reprisk.parquet"
        if os.path.exists(file_path):
            RepRisk_df = pd.read_parquet(file_path)
        else:
            flag = 1
    
    if flag:
        RepRisk_df = pull_RepRisk(start_date=start_date, end_date=end_date, wrds_username=wrds_username)

        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            RepRisk_df.to_parquet(file_dir / 'reprisk.parquet')

    return RepRisk_df


if __name__ == "__main__":
    # Pull and save cache of RepRisk data
    _ = load_RepRisk(data_dir=DATA_DIR, from_cache=True, save_cache=True, start_date=START_DATE, end_date=END_DATE,
                     wrds_username=WRDS_USERNAME)
