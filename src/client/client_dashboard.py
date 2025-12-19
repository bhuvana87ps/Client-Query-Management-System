import streamlit as st
import pandas as pd
import re
from datetime import datetime
from services.db_connection import get_db_connection


# ===================================================
# CLIENT DASHBOARD
# ===================================================
def client_dashboard():

    # ---------------------------------------------------
    # SESSION (already set by login)
    # ---------------------------------------------------
    client_email = st.session_state.get("client_email")
    client_mobile = st.session_state.get("client_mobile")

    if not client_email:
        st.error("Session expired. Please login again.")
        st.stop()

    # ---------------------------------------------------
    # SIDEBAR (CLEAN & COMPACT)
    # ---------------------------------------------------
    with st.sidebar:
        st.markdown("### 👤 Client Profile")
        st.write(f"📧 **{client_email}**")
        st.write(f"📱 **{client_mobile}**")

        with st.expander("🔍 Filters", expanded=True):
            status_filter = st.selectbox(
                "Status", ["All", "Open", "Closed"]
            )

            category_filter = st.selectbox(
                "Category",
                [
                    "All",
                    "Account Suspension",
                    "Billing Problem",
                    "Bug Report",
                    "Data Export",
                    "Feature Request",
                    "Login Issue",
                    "Payment Failure",
                    "Subscription Cancellation",
                    "Technical Support",
                    "UI Feedback",
                ],
            )

            date_range = st.date_input("Date Range", [])

    # ---------------------------------------------------
    # FETCH DATA
    # ---------------------------------------------------
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT * FROM client_queries WHERE client_email=%s",
        conn,
        params=(client_email,),
    )
    conn.close()

    if df.empty:
        st.info("No queries found.")
        return

    df["query_created_time"] = pd.to_datetime(df["query_created_time"])
    df["query_closed_time"] = pd.to_datetime(
        df["query_closed_time"], errors="coerce"
    )

    # ---------------------------------------------------
    # APPLY FILTERS
    # ---------------------------------------------------
    filtered_df = df.copy()

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]

    if len(date_range) == 2:
        start, end = date_range
        filtered_df = filtered_df[
            (filtered_df["query_created_time"].dt.date >= start)
            & (filtered_df["query_created_time"].dt.date <= end)
        ]

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------
    tab_analytics, tab_queries, tab_new = st.tabs(
        ["📊 Client Analytics", "📋 My Queries", "➕ Raise New Query"]
    )

    # ===================================================
    # TAB 1 — CLIENT ANALYTICS
    # ===================================================
    with tab_analytics:
        st.subheader("📊 Client Analytics")

        total_q = len(df)
        open_q = (df["status"] == "Open").sum()
        closed_q = (df["status"] == "Closed").sum()

        df_closed = df[df["status"] == "Closed"].copy()
        if not df_closed.empty:
            df_closed["resolution_days"] = (
                df_closed["query_closed_time"]
                - df_closed["query_created_time"]
            ).dt.days
            avg_res = round(df_closed["resolution_days"].mean(), 1)
        else:
            avg_res = "—"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Queries", total_q)
        c2.metric("Open", open_q)
        c3.metric("Closed", closed_q)
        c4.metric("Avg Resolution (Days)", avg_res)

        st.markdown("#### Queries by Category")
        st.bar_chart(df["category"].value_counts())

        st.markdown("#### Status Distribution")
        st.bar_chart(df["status"].value_counts())

    # ===================================================
    # TAB 2 — MY QUERIES
    # ===================================================
    with tab_queries:
        st.subheader("📋 My Queries")

        if filtered_df.empty:
            st.info("No queries for selected filters.")
            return

        def style_rows(row):
            if row["is_valid_mobile"] == 0:
                return ["background-color:#f8d7da"] * len(row)
            if row["status"] == "Open":
                return ["background-color:#fff3cd"] * len(row)
            if row["status"] == "Closed":
                return ["background-color:#d4edda"] * len(row)
            return [""] * len(row)

        display_cols = [
            "query_id",
            "category",
            "status",
            "query_created_time",
            "query_closed_time",
            "is_valid_mobile",
        ]

        styled_df = (
            filtered_df[display_cols]
            .sort_values("query_created_time", ascending=False)
            .style.apply(style_rows, axis=1)
        )

        st.dataframe(styled_df, use_container_width=True)

        st.markdown(
            """
            🟡 **Open Query**  
            🟢 **Closed Query**  
            🔴 **Invalid Mobile**
            """
        )

        st.download_button(
            "⬇ Download CSV",
            filtered_df.to_csv(index=False),
            "my_queries.csv",
            "text/csv",
        )

    # ===================================================
    # TAB 3 — NEW QUERY
    # ===================================================
    with tab_new:
        st.subheader("➕ Raise New Query")

        def normalize_mobile(m):
            digits = re.sub(r"\D", "", m)
            return digits[-10:] if len(digits) >= 10 else None

        def valid_mobile(m):
            return bool(re.match(r"^[6-9]\d{9}$", m))

        with st.form("new_query"):
            category = st.selectbox(
                "Category",
                [
                    "Account Suspension",
                    "Billing Problem",
                    "Bug Report",
                    "Data Export",
                    "Feature Request",
                    "Login Issue",
                    "Payment Failure",
                    "Subscription Cancellation",
                    "Technical Support",
                    "UI Feedback",
                ],
            )

            heading = st.text_input("Query Heading")
            description = st.text_area("Query Description")
            image = st.file_uploader(
                "Upload Issue Screenshot (Required)",
                type=["png", "jpg", "jpeg"],
            )

            submit = st.form_submit_button("Submit")

        if submit:
            if not heading or len(description) < 10:
                st.error("Provide valid heading & description.")
                return

            if image is None:
                st.error("Issue image is required.")
                return

            nm = normalize_mobile(client_mobile)
            if not nm or not valid_mobile(nm):
                st.error("Invalid registered mobile number.")
                return

            conn = get_db_connection()
            cur = conn.cursor()

            # Generate next CQ ID
            cur.execute(
                "SELECT query_id FROM client_queries ORDER BY query_created_time DESC LIMIT 1"
            )
            last = cur.fetchone()
            next_id = (
                f"CQ{int(last[0][2:]) + 1:03d}"
                if last
                else "CQ001"
            )

            cur.execute(
                """
                INSERT INTO client_queries
                (query_id, client_email, client_mobile,
                 normalized_mobile, is_valid_mobile,
                 category, query_heading, query_description,
                 status, query_created_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'Open',NOW())
                """,
                (
                    next_id,
                    client_email,
                    client_mobile,
                    nm,
                    1,
                    category,
                    heading,
                    description,
                ),
            )

            conn.commit()
            cur.close()
            conn.close()

            st.success("Query submitted successfully!")
            st.rerun()
