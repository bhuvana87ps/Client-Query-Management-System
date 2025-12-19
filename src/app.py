"""
app.py
--------------------------------------------------
Main entry point for
Client Query Management System (CQMS)

Responsibilities:
- App configuration
- Session management
- Sidebar navigation
- Role-based routing
--------------------------------------------------
"""

import streamlit as st


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Client Query Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


# --------------------------------------------------
# SIDEBAR RENDERING
# --------------------------------------------------
def render_sidebar():
    user = st.session_state.get("user")

    with st.sidebar:
        st.title("📊 CQMS")

        if user:
            st.markdown(f"**Logged in as:** `{user['role']}`")
            st.markdown(f"**User:** `{user['username']}`")
            st.divider()

            # Client Navigation
            if user["role"] == "Client":
                if st.button("📝 Submit Query"):
                    st.session_state["page"] = "client_dashboard"

            # Support Navigation
            if user["role"] == "Support":
                if st.button("📂 Query Management"):
                    st.session_state["page"] = "support_dashboard"

            st.divider()

            if st.button("🚪 Logout"):
                st.session_state["user"] = None
                st.session_state["page"] = "login"
                st.rerun()

        else:
            st.info("Please login to continue.")


# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------
def route_page():
    page = st.session_state.get("page")

    if page == "login":
        from auth.login import login_page
        login_page()

    elif page == "client_dashboard":
        from client.client_dashboard import client_dashboard
        client_dashboard()

    elif page == "support_dashboard":
        from support.support_dashboard import support_dashboard
        support_dashboard()

    else:
        st.error("Page not found.")


# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
render_sidebar()
route_page()
