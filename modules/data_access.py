import streamlit as st
import pandas as pd
from .db_connector import read_sql_df
from .sqls import SQL_SALES_HISTORY_BOOSTERS, SQL_SALES_HISTORY_SCM, SQL_PRODUCT_PRICE, SQL_CURRENT_INVENTORY

@st.cache_data(show_spinner=False)
def load_sales_history_combined() -> pd.DataFrame:
    """boosters(ERP) + scm(SCM) 판매이력 병합"""
    df_boosters = read_sql_df(SQL_SALES_HISTORY_BOOSTERS, db_type="erp")
    df_scm = read_sql_df(SQL_SALES_HISTORY_SCM, db_type="scm")
    df = pd.concat([df_boosters, df_scm], ignore_index=True)
    df = df.dropna(subset=["ym", "product_code"]).copy()
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)
    return df

@st.cache_data(show_spinner=False)
def load_product_prices() -> pd.DataFrame:
    return read_sql_df(SQL_PRODUCT_PRICE, db_type="erp")

@st.cache_data(show_spinner=False)
def load_current_inventory() -> pd.DataFrame:
    df = read_sql_df(SQL_CURRENT_INVENTORY, db_type="scm")
    df["stock_qty"] = pd.to_numeric(df["stock_qty"], errors="coerce").fillna(0).astype(int)
    return df
