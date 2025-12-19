import pandas as pd
from services.db_connection import get_db_connection


# --------------------------------------------------
# Load all query data
# --------------------------------------------------
def load_queries():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM client_queries", conn)
    conn.close()

    df["query_created_time"] = pd.to_datetime(df["query_created_time"])
    df["query_closed_time"] = pd.to_datetime(
        df["query_closed_time"], errors="coerce"
    )

    df["query_age_days"] = (
        (df["query_closed_time"].fillna(pd.Timestamp.now()))
        - df["query_created_time"]
    ).dt.days

    return df


# --------------------------------------------------
# Service Efficiency Metrics
# --------------------------------------------------
def service_efficiency_metrics(df):
    closed_df = df[df["status"] == "Closed"].copy()

    if closed_df.empty:
        return {
            "avg_resolution": None,
            "median_resolution": None
        }

    resolution_days = (
        closed_df["query_closed_time"]
        - closed_df["query_created_time"]
    ).dt.days

    return {
        "avg_resolution": round(resolution_days.mean(), 2),
        "median_resolution": int(resolution_days.median())
    }


# --------------------------------------------------
# Support Load Monitoring
# --------------------------------------------------
def support_load_metrics(df):
    return (
        df.groupby("category")
        .size()
        .reset_index(name="query_count")
        .sort_values("query_count", ascending=False)
    )


# --------------------------------------------------
# Agent Workload Analytics
# --------------------------------------------------
def agent_workload(df):
    closed = df[df["status"] == "Closed"]

    leaderboard = (
        closed.groupby("assigned_support_id")
        .agg(
            closed_queries=("query_id", "count"),
            avg_resolution_days=("query_age_days", "mean")
        )
        .reset_index()
        .sort_values("closed_queries", ascending=False)
    )

    leaderboard["avg_resolution_days"] = leaderboard[
        "avg_resolution_days"
    ].round(1)

    return leaderboard


# --------------------------------------------------
# SLA Breach Detection
# --------------------------------------------------
def sla_breaches(df, sla_days=3):
    return df[
        (df["status"] != "Closed") &
        (df["query_age_days"] > sla_days)
    ][
        ["query_id", "assigned_support_id", "query_age_days", "status"]
    ]
