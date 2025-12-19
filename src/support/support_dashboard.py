import streamlit as st
import pandas as pd
from datetime import datetime
from services.db_connection import get_db_connection


# ===================================================
# SUPPORT DASHBOARD
# ===================================================
def support_dashboard():

    # ---------------------------------------------------
    # SESSION VALIDATION
    # ---------------------------------------------------
    user = st.session_state.get("user")

    if not user or user.get("role") != "Support":
        st.error("Unauthorized access.")
        st.stop()

    support_id = user.get("username")  # e.g. S001

    st.markdown(f"## 🧑‍💻 Support Dashboard — {support_id}")

    # ---------------------------------------------------
    # FETCH ALL QUERIES
    # ---------------------------------------------------
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM client_queries", conn)
    conn.close()

    if df.empty:
        st.info("No queries available.")
        return

    df["query_created_time"] = pd.to_datetime(df["query_created_time"])
    df["query_closed_time"] = pd.to_datetime(
        df["query_closed_time"], errors="coerce"
    )

    # Query age
    df["query_age_days"] = (
        (df["query_closed_time"].fillna(pd.Timestamp.now()))
        - df["query_created_time"]
    ).dt.days

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------
    tab_open, tab_progress, tab_closed, tab_analytics = st.tabs(
        ["🟢 Open Queue", "🟡 My In Progress", "🔵 Closed Queries", "📊 Team Analytics"]
    )

    # ===================================================
    # 🟢 OPEN QUEUE
    # ===================================================
    with tab_open:
        st.subheader("🟢 Open Queue")

        open_df = df[
            (df["status"] == "Open")
            & (df["assigned_support_id"].isna())
        ]

        if open_df.empty:
            st.success("No unassigned open queries 🎉")
        else:
            for _, row in open_df.iterrows():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([4, 2, 2])

                    c1.markdown(
                        f"""
                        **{row['query_id']}**  
                        📂 {row['category']}  
                        ⏳ {row['query_age_days']} days
                        """
                    )

                    if c3.button(
                        "Pick",
                        key=f"pick_{row['query_id']}",
                    ):
                        conn = get_db_connection()
                        cur = conn.cursor()
                        cur.execute(
                            """
                            UPDATE client_queries
                            SET assigned_support_id=%s,
                                status='In Progress'
                            WHERE query_id=%s
                            """,
                            (support_id, row["query_id"]),
                        )
                        conn.commit()
                        cur.close()
                        conn.close()

                        st.success("Query picked successfully.")
                        st.rerun()

    # ===================================================
    # 🟡 MY IN PROGRESS
    # ===================================================
    with tab_progress:
        st.subheader("🟡 My In Progress")

        progress_df = df[
            (df["status"] == "In Progress")
            & (df["assigned_support_id"] == support_id)
        ]

        if progress_df.empty:
            st.info("No queries in progress.")
        else:
            for _, row in progress_df.iterrows():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([4, 2, 2])

                    c1.markdown(
                        f"""
                        **{row['query_id']}**  
                        📂 {row['category']}  
                        ⏳ {row['query_age_days']} days
                        """
                    )

                    if c3.button(
                        "Close",
                        key=f"close_{row['query_id']}",
                    ):
                        conn = get_db_connection()
                        cur = conn.cursor()
                        cur.execute(
                            """
                            UPDATE client_queries
                            SET status='Closed',
                                query_closed_time=NOW()
                            WHERE query_id=%s
                            """,
                            (row["query_id"],),
                        )
                        conn.commit()
                        cur.close()
                        conn.close()

                        st.success("Query closed.")
                        st.rerun()

    # ===================================================
    # 🔵 CLOSED QUERIES
    # ===================================================
    with tab_closed:
        st.subheader("🔵 Closed Queries")

        closed_df = df[df["status"] == "Closed"].copy()

        if closed_df.empty:
            st.info("No closed queries.")
        else:
            closed_df["resolution_days"] = (
                closed_df["query_closed_time"]
                - closed_df["query_created_time"]
            ).dt.days

            st.dataframe(
                closed_df[
                    [
                        "query_id",
                        "category",
                        "assigned_support_id",
                        "resolution_days",
                    ]
                ]
                .sort_values("resolution_days", ascending=False),
                use_container_width=True,
            )

    # ===================================================
    # 📊 TEAM ANALYTICS
    # ===================================================
    with tab_analytics:
        st.subheader("📊 Support Team Analytics")

        total_agents = df["assigned_support_id"].nunique()
        open_q = (df["status"] == "Open").sum()
        in_prog_q = (df["status"] == "In Progress").sum()
        closed_q = (df["status"] == "Closed").sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Agents", total_agents)
        c2.metric("Open", open_q)
        c3.metric("In Progress", in_prog_q)
        c4.metric("Closed", closed_q)

        # Agent leaderboard
        st.markdown("### 🏆 Agent Leaderboard")

        leaderboard = (
            df[df["status"] == "Closed"]
            .groupby("assigned_support_id")
            .agg(
                closed_queries=("query_id", "count"),
                avg_days=("query_age_days", "mean"),
            )
            .reset_index()
            .sort_values("closed_queries", ascending=False)
        )

        leaderboard["avg_days"] = leaderboard["avg_days"].round(1)
        leaderboard.index += 1

        st.dataframe(leaderboard, use_container_width=True)

        # SLA
        st.markdown("### ⏱ SLA Breaches (Target: 3 days)")

        sla_df = df[
            (df["status"] != "Closed") & (df["query_age_days"] > 3)
        ]

        if sla_df.empty:
            st.success("No SLA breaches 🎉")
        else:
            st.warning("SLA Breaches Detected")
            st.dataframe(
                sla_df[
                    [
                        "query_id",
                        "assigned_support_id",
                        "query_age_days",
                        "status",
                    ]
                ],
                use_container_width=True,
            )
