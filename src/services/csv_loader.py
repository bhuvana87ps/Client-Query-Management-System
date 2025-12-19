"""
csv_loader.py
--------------------------------------------------
Loads historical client query data from CSV
into MySQL database for CQMS project.

Run using:
    python -m src.services.csv_loader
--------------------------------------------------
"""

import pandas as pd
from datetime import datetime
from .db_connection import get_db_connection, close_db_connection

# --------------------------------------------------
# CSV FILE PATH
# --------------------------------------------------
CSV_PATH = "data/raw/client_queries_5000.csv"


def safe_datetime(val):
    """
    Convert pandas Timestamp to Python datetime
    Return None if NaT / missing
    """
    if pd.isna(val):
        return None
    return val.to_pydatetime()


# --------------------------------------------------
# LOAD CSV INTO MYSQL
# --------------------------------------------------
def load_csv():
    print("📄 Reading CSV file...")
    df = pd.read_csv(CSV_PATH)

    # Rename columns to match DB schema
    df.rename(columns={
        "date_raised": "query_created_time",
        "date_closed": "query_closed_time"
    }, inplace=True)

    # Convert to datetime (Pandas)
    df["query_created_time"] = pd.to_datetime(df["query_created_time"])
    df["query_closed_time"] = pd.to_datetime(df["query_closed_time"], errors="coerce")

    # Fill required fields
    df["status"] = df["status"].str.strip()
    df["category"] = df["query_heading"]   # using heading as category
    df["issue_image_path"] = None

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT IGNORE INTO client_queries (
            query_id,
            client_email,
            client_mobile,
            category,
            query_heading,
            query_description,
            status,
            query_created_time,
            query_closed_time,
            issue_image_path
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    inserted = 0

    for _, row in df.iterrows():
        cursor.execute(insert_sql, (
            row["query_id"],
            row["client_email"],
            str(row["client_mobile"]),
            row["category"],
            row["query_heading"],
            row["query_description"],
            row["status"],
            safe_datetime(row["query_created_time"]),
            safe_datetime(row["query_closed_time"]),
            None
        ))
        inserted += 1

    conn.commit()
    close_db_connection(conn, cursor)

    print(f"✅ CSV load complete. Records processed: {inserted}")


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    load_csv()
