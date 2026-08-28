import streamlit as st

from sql_page import sql_page


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="International Debt Analysis",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# RUN SQL PAGE
# ============================================================

sql_page()