# utils/date_utils.py
import pandas as pd
from datetime import datetime


# -----------------------------
# Safe datetime conversion
# -----------------------------
def to_datetime(series):
    return pd.to_datetime(series, errors="coerce")


# -----------------------------
# Resolution Time (days)
# -----------------------------
def calculate_resolution_days(created, closed):
    if pd.isna(created) or pd.isna(closed):
        return None
    return (closed - created).days


# -----------------------------
# Query Age (Open / In Progress)
# -----------------------------
def calculate_query_age(created):
    if pd.isna(created):
        return None
    return (datetime.now() - created).days
