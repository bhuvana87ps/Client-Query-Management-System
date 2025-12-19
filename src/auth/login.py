"""
login.py
--------------------------------------------------
Streamlit Login Page for
Client Query Management System (CQMS)

This file exposes login_page() function
(required by app.py router)
--------------------------------------------------
"""

import streamlit as st
from auth.auth_utils import login_user


# --------------------------------------------------
# LOGIN PAGE FUNCTION (IMPORTANT)
# --------------------------------------------------
def login_page():
    st.title("🔐 Client Query Management System")
    st.subheader("Login")

    # Initialize session state if not present
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # -------------------------------
    # LOGIN FORM
    # -------------------------------
    with st.form("login_form"):
        identifier = st.text_input(
            "Username / Email / Mobile Number",
            placeholder="Enter username, email, or mobile"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Login As",
            ["Client", "Support"]
        )

        submit = st.form_submit_button("Login")

    # -------------------------------
    # LOGIN LOGIC
    # -------------------------------
    if submit:
        if not identifier or not password:
            st.error("Please enter all required fields.")
            return

        success, result = login_user(identifier, password, role)

        if success:
            st.session_state["user"] = result
            st.session_state["page"] = (
                "client_dashboard" if role == "Client" else "support_dashboard"
            )
            st.success(f"Welcome, {result['username']}!")
            st.rerun()
        else:
            st.error(result)

    # -------------------------------
    # FOOTER
    # -------------------------------
    st.markdown("---")
    st.caption("CQMS • Secure Database-Level Authentication")
